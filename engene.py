# engene.py
from groq import Groq
from config import GROQ_API_KEY, GROQ_MODEL, CONTEXT_WINDOW, SIMILARITY_THRESHOLD, SYNONYMS
from processor import clean_text
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Initialize Groq Client
client = Groq(api_key=GROQ_API_KEY)

def find_best_answer(query, chunks, chat_history=[]):
    processed_query = query.lower()

    # --- 1. THE ALBUM "CHEAT SHEET" ---
    # This forces the search engine to prioritize these specific OCR pages
    # --- 1. THE ALBUM "CHEAT SHEET" ---
    # Maps every album in the book to its specific high-quality OCR page
    album_map = {
        "author":"PAGE 32",
        "book release date": "PAGE 32",
        "2 cool 4 skool": "PAGE 82",
        "o!rul8,2?": "PAGE 93",
        "oh are you late too": "PAGE 93",
        "skool luv affair": "PAGE 102",
        "sla": "PAGE 102",
        "dark & wild": "PAGE 114",
        "dark&wild": "PAGE 114",
        "dark and wild": "PAGE 114",
        "the most beautiful moment in life pt.1": "PAGE 135",
        "hwayangyeonhwa pt.1": "PAGE 135",
        "hyyh pt.1": "PAGE 135",
        "the most beautiful moment in life pt.2": "PAGE 160",
        "hyyh pt.2": "PAGE 160",
        "hwayangyeonhwa pt.2": "PAGE 160",
        "young forever": "PAGE 176",
        "hyyh young forever": "PAGE 176",
        "hyyh pt.3": "PAGE 176",
        "wings": "PAGE 192",
        "you never walk alone": "PAGE 217",
        "ynwa": "PAGE 217",
        "love yourself her": "PAGE 233",
        "ly her": "PAGE 233",
        "love yourself tear": "PAGE 258",
        "ly tear": "PAGE 258",
        "love yourself answer": "PAGE 270",
        "ly answer": "PAGE 270",
        "map of the soul persona": "PAGE 292",
        "persona": "PAGE 292",
        "mots persona": "PAGE 292",
        "map of the soul 7": "PAGE 324",
        "mots 7": "PAGE 324",
        "dynamite": "PAGE 348",
        "be": "PAGE 353",
        "butter": "PAGE 371 PAGE 372",
        "proof": "PAGE 398 PAGE 399"
    }

    # Identify if the user is asking for a list
    is_list_query = any(word in processed_query for word in ["tracklist", "songs", "list", "tracks", "discography"])

    # Filter out Table of Contents (TOC) for list queries to avoid distraction
    if is_list_query:
        search_chunks = [c for c in chunks if "CONTENTS" not in c and "CHAPTER" not in c]
        # Inject the specific page number into the search query if an album is mentioned
        for album, page in album_map.items():
            if album in processed_query:
                # This makes the TF-IDF search "gravitate" toward your OCR blocks
                processed_query += f" --- DATA FROM {page} ---"
    else:
        search_chunks = chunks

    # --- 2. SEARCH LOGIC (TF-IDF) ---
    cleaned_chunks = [c.lower() for c in search_chunks]
    vectorizer = TfidfVectorizer(ngram_range=(1, 2))

    # Fit and transform the context chunks + the query
    tfidf_matrix = vectorizer.fit_transform(cleaned_chunks + [processed_query])
    scores = cosine_similarity(tfidf_matrix[-1], tfidf_matrix[:-1])

    # Massive boost for OCR pages (DATA FROM PAGE) during tracklist searches
    if is_list_query:
        for i, chunk in enumerate(search_chunks):
            if "--- DATA FROM PAGE" in chunk:
                scores[0][i] *= 5.0  # Force the OCR page to the top

    best_idx = scores.argmax()

    # --- 3. CONTEXT BUILDING ---
    # We only need the specific page for a tracklist (window=0 or 1)
    window = 3 if is_list_query else CONTEXT_WINDOW
    start = max(0, best_idx - window)
    end = min(len(search_chunks), best_idx + window + 1)
    raw_knowledge = "\n".join(search_chunks[start:end])

    # --- 4. THE "CODE-BREAKER" SYSTEM PROMPT ---
    system_prompt = (
        "You are an expert BTS historian providing information based on the official "
        "biography 'Beyond The Story'.\n\n"

        "CRITICAL FORMATTING RULES:\n"
        "1. Never mention technical terms like '--- DATA FROM PAGE ---', 'OCR', or 'cache'.\n"
        "2. If the user asks for a tracklist, you MUST use a vertical bulleted list (one song per line).\n"
        "3. NEVER present tracks in a paragraph or a single line separated by dots (•).\n"
        "4. For multi-CD albums (like Proof), use bold headers: **CD 1**, **CD 2**, etc.\n"
        "5. If the user requests multiple albums, separate them clearly by the Album Name and Release Date.\n"
        "6. Use the 'discography' sections from the book to ensure 100% accuracy.\n\n"

        "EXAMPLE FORMAT:\n"
        "**ALBUM NAME** (YYYY. MM. DD)\n\n"
        "**CD 1**\n"
        "* Song Title 1\n"
        "* Song Title 2\n"
        "**CD 2**\n"
        "* Song Title 3"
    )

    # --- 5. GENERATION ---
    messages = [{"role": "system", "content": system_prompt}]

    # Add relevant chat history for memory
    for msg in chat_history[-3:]:
        messages.append({"role": msg["role"], "content": msg["content"]})

    messages.append({
        "role": "user",
        "content": f"BOOK CONTEXT:\n{raw_knowledge}\n\nQUESTION: {query}"
    })

    try:
        completion = client.chat.completions.create(
            model=GROQ_MODEL,
            messages=messages,
            temperature=0  # Keep it strictly factual
        )
        return completion.choices[0].message.content, raw_knowledge
    except Exception as e:
        return f"Error connecting to Groq: {str(e)}", "No context available."