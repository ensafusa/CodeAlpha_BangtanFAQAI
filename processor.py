# processor.py
import fitz
import re
import os

def clean_text(text):
    text = re.sub(r'(\b\w+)\s+(?=\w\b)', r'\1', text)
    return text.strip()

def get_book_chunks(pdf_path):
    chunks = []
    cache_file = "full_book_cache.txt"

    # 1. Load the Main Book Text (from cache or PDF)
    if os.path.exists(cache_file):
        with open(cache_file, "r", encoding="utf-8") as f:
            chunks = f.read().split("---PAGE_BREAK---")
    else:
        doc = fitz.open(pdf_path)
        full_text_to_save = ""
        for page in doc:
            text = page.get_text("text").strip()
            if len(text) > 20:
                cleaned = clean_text(text)
                chunks.append(cleaned)
                full_text_to_save += cleaned + "---PAGE_BREAK---"
        with open(cache_file, "w", encoding="utf-8") as f:
            f.write(full_text_to_save)

    # ==========================================
    # 2. INSERT YOUR OCR DATA BLOCK HERE
    # ==========================================
    if os.path.exists("ocr_cache.txt"):
        with open("ocr_cache.txt", "r", encoding="utf-8") as f:
            ocr_data = f.read()
            # Split by your custom header
            ocr_chunks = ocr_data.split("--- DATA FROM")
            # Filter and add to the main chunks list
            chunks.extend([c.strip() for c in ocr_chunks if len(c.strip()) > 10])

    return chunks