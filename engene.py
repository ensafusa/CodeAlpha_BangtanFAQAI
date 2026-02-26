# engene.py
from groq import Groq
from config import GROQ_API_KEY, GROQ_MODEL, CONTEXT_WINDOW, SIMILARITY_THRESHOLD, SYNONYMS
from processor import clean_text
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

client = Groq(api_key=GROQ_API_KEY)

def find_best_answer(query, chunks, chat_history=[]):
    # --- 1. SEARCH LOGIC ---
    cleaned_chunks = [clean_text(c) for c in chunks]
    processed_query = query.lower()

    # Discography boost
    if any(word in processed_query for word in ["album", "song", "track", "list", "single"]):
        processed_query += " discography tracklist album type release date"

    vectorizer = TfidfVectorizer(ngram_range=(1, 2))
    tfidf_matrix = vectorizer.fit_transform(cleaned_chunks + [processed_query])
    scores = cosine_similarity(tfidf_matrix[-1], tfidf_matrix[:-1])
    best_idx = scores.argmax()

    # --- 2. CONTEXT BUILDING ---
    window = CONTEXT_WINDOW + 5 if "album" in processed_query else CONTEXT_WINDOW
    start = max(0, best_idx - window)
    end = min(len(chunks), best_idx + window + 5)
    raw_knowledge = "\n".join(chunks[start:end])

    # --- 3. MEMORY & GENERATION ---
    # We build the message list properly BEFORE calling the API
    messages = [
        {"role": "system", "content": "You are a BTS expert. Use the BOOK CONTEXT and chat history to answer. BTS has 7 members: RM, Jin, SUGA, j-hope, Jimin, V, Jungkook."}
    ]

    # Add last 3 messages for conversational context
    for msg in chat_history[-3:]:
        messages.append({"role": msg["role"], "content": msg["content"]})

    # Add the current context and question
    messages.append({
        "role": "user",
        "content": f"BOOK CONTEXT:\n{raw_knowledge}\n\nQUESTION: {query}"
    })

    try:
        completion = client.chat.completions.create(
            model=GROQ_MODEL,
            messages=messages,
            temperature=0.3
        )
        return completion.choices[0].message.content, raw_knowledge
    except Exception as e:
        return f"Brain Error: {str(e)}", raw_knowledge