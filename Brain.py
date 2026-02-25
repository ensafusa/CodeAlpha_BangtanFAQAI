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

# --- NLP CLEANING FUNCTION ---
def clean_text(text):
    # Convert to lowercase and tokenize
    stop_words = set(stopwords.words('english'))
    words = word_tokenize(text.lower())
    # Remove non-alphabetical characters and stop words
    cleaned = [w for w in words if w.isalpha() and w not in stop_words]
    return " ".join(cleaned)

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

# --- THE SEARCH ENGINE ---
def find_answer(user_question, pages):
    # 1. Break pages into smaller paragraphs for better precision
    all_paragraphs = []
    for page in pages:
        # Split by double newlines or large spaces (common for paragraphs)
        parts = page.split('\n\n')
        all_paragraphs.extend([p.strip() for p in parts if len(p.strip()) > 50])

    # 2. Preprocess
    cleaned_paragraphs = [clean_text(p) for p in all_paragraphs]
    cleaned_query = clean_text(user_question)

    # 3. Vectorization (Math)
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(cleaned_paragraphs + [cleaned_query])

    # 4. Cosine Similarity
    similarity_scores = cosine_similarity(tfidf_matrix[-1], tfidf_matrix[:-1])
    best_match_index = similarity_scores.argmax()

    # If the score is very low, the AI is just guessing
    if similarity_scores[0][best_match_index] < 0.15:
        return "I'm sorry, I couldn't find a specific section in the book that answers that."

    return all_paragraphs[best_match_index]


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