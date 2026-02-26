# processor.py
import fitz  # PyMuPDF
import easyocr
import numpy as np
import cv2
from config import SYNONYMS

# Initialize the OCR reader once
reader = easyocr.Reader(['en'])

def clean_text(text):
    import re
    text = re.sub(r'(\b\w+)\s+(?=\w\b)', r'\1', text)
    text = text.replace("jim ", "jimin ").replace("jung kook", "jungkook")
    return text.strip()

def get_book_chunks(pdf_path):
    all_lines = []
    try:
        doc = fitz.open(pdf_path)
        for page_num in range(len(doc)):
            page = doc[page_num]

            # 1. Try standard text extraction first
            text = page.get_text().strip()

            # 2. If the page is mostly an image (like the BE tracklist)
            if len(text) < 50:
                pix = page.get_pixmap()
                img = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.h, pix.w, pix.n)
                # Use EasyOCR to read the image text
                ocr_results = reader.readtext(img, detail=0)
                text = " ".join(ocr_results)

            if text:
                all_lines.append(clean_text(text))
        return all_lines
    except Exception as e:
        print(f"Error: {e}")
        return []