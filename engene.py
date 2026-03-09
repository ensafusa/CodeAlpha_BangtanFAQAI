import json
import re

from groq import Groq

from config import GROQ_API_KEY, GROQ_MODEL, CONTEXT_WINDOW, SIMILARITY_THRESHOLD, SYNONYMS
from processor import clean_text
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

client = Groq(api_key=GROQ_API_KEY)

def normalize_string(text):
    text = text.lower().replace(":", " ")
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def format_json_response(album_name, data):
    release_date = data.get('release_date') or data.get('RELEASE_DATE', 'N/A')
    album_type= data.get('type') or data.get('TYPE', 'N/A')
    output = f"**{album_name.upper()}** **({album_type.upper()})** ({release_date})\n\n"

    for key, value in data.items():
        if key.lower() not in ['type', 'release_date']:

            if "cd" in key.lower():
                output += f"\n**{key.upper()}**\n"

            if isinstance(value, list):
                for track in value:
                    output += f"* {track}\n"
            else:
                output += f"* {value}\n"

    return output

def find_best_answer(query, chunks, chat_history=[]):
    processed_query = normalize_string(query)

    tracklist_keywords = ["tracklist", "songs", "tracks", "list of songs"]
    is_list_request = any(word in processed_query for word in tracklist_keywords)

    try:
        with open('discography.json', 'r') as f:
            disco_data = json.load(f)
        sorted_albums = sorted(disco_data.keys(), key=len, reverse=True)

        for album_name, data in disco_data.items():
            normalized_album = normalize_string(album_name)
            print(album_name)
            print(normalized_album)
            if normalized_album in processed_query and is_list_request:
                return format_json_response(album_name, data), "JSON Ground Truth"

    except Exception as e:
        print(f"Error: {e}")

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

    is_list_query = any(word in processed_query for word in ["tracklist", "songs", "list", "tracks", "discography"])

    if is_list_query:
        search_chunks = [c for c in chunks if "CONTENTS" not in c and "CHAPTER" not in c]
        for album, page in album_map.items():
            if album in processed_query:
                processed_query += f" --- DATA FROM {page} ---"
    else:
        search_chunks = chunks

    cleaned_chunks = [c.lower() for c in search_chunks]
    vectorizer = TfidfVectorizer(ngram_range=(1, 2))

    tfidf_matrix = vectorizer.fit_transform(cleaned_chunks + [processed_query])
    scores = cosine_similarity(tfidf_matrix[-1], tfidf_matrix[:-1])

    if is_list_query:
        for i, chunk in enumerate(search_chunks):
            if "--- DATA FROM PAGE" in chunk:
                scores[0][i] *= 5.0

    best_idx = scores.argmax()

    window = 3 if is_list_query else CONTEXT_WINDOW
    start = max(0, best_idx - window)
    end = min(len(search_chunks), best_idx + window + 1)
    raw_knowledge = "\n".join(search_chunks[start:end])

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

    messages = [{"role": "system", "content": system_prompt}]

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
            temperature=0
        )
        return completion.choices[0].message.content, raw_knowledge
    except Exception as e:
        return f"Error connecting to Groq: {str(e)}", "No context available."