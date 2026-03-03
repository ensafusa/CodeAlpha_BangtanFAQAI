import fitz # PyMuPDF
import easyocr
import numpy as np
import os

# Your provided page numbers (will be converted to 0-based index)
image_pages = [32, 82, 93, 102, 114, 135, 160, 176, 192, 217, 233, 258, 270, 292, 324, 348, 353, 371, 372, 398, 399]

def generate_ocr():
    print("--- 🚀 Initializing EasyOCR Engine ---")
    reader = easyocr.Reader(['en'])

    doc = fitz.open("Beyond-the-Story-_Retail_-3.pdf")
    all_extracted_text = ""

    for pg_num in image_pages:
        idx = pg_num - 1 # Adjusting for 0-based indexing
        print(f"Scanning Page {pg_num}...")

        try:
            page = doc[idx]
            # Zoom 2x for high-quality OCR (important for tracklists!)
            pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
            img = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.h, pix.w, pix.n)

            result = reader.readtext(img, detail=0)

            # Format the output so the AI knows exactly where the info came from
            page_content = f"\n--- DATA FROM PAGE {pg_num} ---\n" + " ".join(result) + "\n"
            all_extracted_text += page_content

        except Exception as e:
            print(f"❌ Error on page {pg_num}: {e}")

    # Save to ocr_cache.txt
    with open("ocr_cache.txt", "w", encoding="utf-8") as f:
        f.write(all_extracted_text)

    print("\n--- ✅ Done! ocr_cache.txt created with your specific pages. ---")

if __name__ == "__main__":
    generate_ocr()