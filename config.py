# config.py

PDF_PATH = "Beyond-the-Story-_Retail_-3.pdf"

# --- API KEYS ---
# Get your key at https://console.groq.com/keys
GROQ_MODEL = "llama-3.3-70b-versatile"
GROQ_API_KEY = "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" # Paste your key here

CONTEXT_WINDOW = 10 # Larger window for album lists
SIMILARITY_THRESHOLD = 0.03 # More lenient for OCR text

# Rules for the AI to understand the subject
SYNONYMS = {
    "bangtan": "bts",
    "seokjin": "jin",
    "namjoon": "rm",
    "yoongi": "suga",
    "hoseok": "j-hope",
    "taehyung": "v",
    "jungkook": "jungkook",
    "bulletproof": "bts"
}
