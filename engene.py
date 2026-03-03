# engene.py
from groq import Groq
from config import GROQ_API_KEY, GROQ_MODEL, CONTEXT_WINDOW, SIMILARITY_THRESHOLD, SYNONYMS
from processor import clean_text
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Initialize Groq Client
client = Groq(api_key=GROQ_API_KEY)

def find_best_answer(query, chunks, chat_history=[]):
    # --- 1. SEARCH LOGIC ---
    processed_query = query.lower()

    # Standardizing synonyms (e.g., "Namjoon" -> "RM")
    for word, replacement in SYNONYMS.items():
        processed_query = processed_query.replace(word, replacement)

    # Keyword check for specialized OCR data (Fixed NameError scope)
    track_keywords = ["tracklist", "songs", "album", "discography", "single", "list"]
    is_tracklist_query = False
    for word in track_keywords:
        if word in processed_query:
            is_tracklist_query = True
            break

    # Inside find_best_answer
    if any(word in processed_query for word in track_keywords):
        # If they ask for "BE", specifically add that to the search string
        # to help the TF-IDF find the page with "BE" in the header.
        if "be" in processed_query.split():
            processed_query += " album be tracklist"

    # If it's an album-related query, we boost the search terms
    if is_tracklist_query:
        search_terms = processed_query + " tracklist songs list track info discography"
    else:
        search_terms = processed_query

    # TF-IDF Vectorization
    cleaned_chunks = [c.lower() for c in chunks]
    vectorizer = TfidfVectorizer(ngram_range=(1, 2))
    tfidf_matrix = vectorizer.fit_transform(cleaned_chunks + [search_terms])

    # Calculate similarity between query and book chunks
    scores = cosine_similarity(tfidf_matrix[-1], tfidf_matrix[:-1])
    best_idx = scores.argmax()

    # --- 2. CONTEXT BUILDING ---
    # We use a smaller window to stay within Groq's token limits (413 Request Entity Too Large)
    # But we give slightly more room for tracklist queries
    window = 3 if is_tracklist_query else CONTEXT_WINDOW

    start = max(0, best_idx - window)
    end = min(len(chunks), best_idx + window + 1)

    # Join the chunks into one block of text for the AI to read
    raw_knowledge = "\n".join(chunks[start:end])

    # --- 3. GENERATION ---
    messages = [
        {
            "role": "system",
            "content": "You are an expert on BTS and the book 'Beyond the Story'. Use the provided BOOK CONTEXT to answer accurately. If the answer isn't in the context, use your knowledge but mention it's supplementary."
        }
    ]

    # Add last 3 messages from history for conversational continuity
    for msg in chat_history[-3:]:
        messages.append({"role": msg["role"], "content": msg["content"]})

    # Add the current context and user question
    messages.append({
        "role": "user",
        "content": f"BOOK CONTEXT:\n{raw_knowledge}\n\nQUESTION: {query}"
    })

    try:
        completion = client.chat.completions.create(
            model=GROQ_MODEL,
            messages=messages,
            temperature=0.2 # Lower temperature for factual accuracy
        )

        answer = completion.choices[0].message.content
        return answer, raw_knowledge

    except Exception as e:
        return f"Error connecting to Groq: {str(e)}", "No context available."