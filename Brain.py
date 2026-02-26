import PyPDF2
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

try:
    nltk.data.find('tokenizers/punkt_tab')
except LookupError:
    nltk.download('punkt_tab')

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

import re

# Add this global mapping
SYNONYMS = {
    "bangtan": "bts",
    "boys": "bts",
    "bulletproof": "bts",
    "beyond the scene": "bts",
    "seokjin": "jin",
    "namjoon": "rm",
    "yoongi": "suga",
    "hoseok": "j-hope",
    "jimin": "jimin",
    "taehyung": "v",
    "jungkook": "jungkook"
}

def clean_text(text):
    stop_words = set(stopwords.words('english'))
    # Remove weird PDF spacing issues (e.g., "f ateful" -> "fateful")
    # This regex looks for letters separated by a single space that should be joined
    text = re.sub(r'(\b[a-z])\s+(?=[a-z]\b)', r'\1', text.lower())

    words = word_tokenize(text.lower())
    cleaned = []
    for w in words:
        if w.isalpha() and w not in stop_words:
            # APPLY SYNONYM MAPPING
            word_to_add = SYNONYMS.get(w, w)
            cleaned.append(word_to_add)
    return " ".join(cleaned)

#___THE SEARCH ENGENE___
def find_answer(user_question, pages):
    all_chunks = []
    for page in pages:
        # Filter out page numbers or very short headers
        lines = [line.strip() for line in page.split('\n') if len(line.strip()) > 5]
        all_chunks.extend(lines)

    cleaned_chunks = [clean_text(c) for c in all_chunks]
    cleaned_query = clean_text(user_question)

    vectorizer = TfidfVectorizer(ngram_range=(1, 2))
    tfidf_matrix = vectorizer.fit_transform(cleaned_chunks + [cleaned_query])

    similarity_scores = cosine_similarity(tfidf_matrix[-1], tfidf_matrix[:-1])
    best_match_index = similarity_scores.argmax()

    if similarity_scores[0][best_match_index] < 0.1:
        return "I'm sorry, the book doesn't seem to mention that specifically."

    # --- THE CONTEXT UPGRADE ---
    # Grab the best line and a few lines around it for context
    start = max(0, best_match_index - 3)
    end = min(len(all_chunks), best_match_index + 4)

    # Join them together into a paragraph
    context_snippet = "\n".join(all_chunks[start:end])

    return context_snippet

# --- PDF EXTRACTION ---
def extract_text_from_pdf(file_path):
    print(f"Reading {file_path}... This may take a moment.")
    text_chunks = []
    try:
        with open(file_path, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text and len(page_text.strip()) > 20: # Skip empty/tiny pages
                    text_chunks.append(page_text)
        print(f"Success! Loaded {len(text_chunks)} pages.")
        return text_chunks
    except Exception as e:
        print(f"Error: {e}")
        return []

# --- EXECUTION ---
if __name__ == "__main__":
    # 1. Update this to your actual PDF name!
    pdf_path = "Beyond-the-Story-_Retail_-3.pdf"
    book_chunks = extract_text_from_pdf(pdf_path)

    if book_chunks:
        print("\nBangtan AI is Ready! Type 'quit' to exit.")
        while True:
            query = input("\nYour Question: ")
            if query.lower() == 'quit':
                break

            answer = find_answer(query, book_chunks)
            print("\n[AI Response from Book]:")
            print(answer.strip())