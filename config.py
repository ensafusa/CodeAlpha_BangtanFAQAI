import os
from dotenv import load_dotenv

load_dotenv()


GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = "llama-3.1-8b-instant"
#GROQ_MODEL = "llama-3.3-70b-versatile"

if GROQ_API_KEY:
    print(f"--- [SUCCESS] Groq API Key loaded (starts with: {GROQ_API_KEY[:6]}...) ---")
else:
    print("--- [ERROR] No API Key found! Check your .env file placement. ---")

PDF_PATH = "Beyond-the-Story-_Retail_-3.pdf"

CONTEXT_WINDOW = 3
SIMILARITY_THRESHOLD = 0.03

SYNONYMS = {
    "bangtan": "bts",
    "seokjin": "jin",
    "namjoon": "rm",
    "yoongi": "suga",
    "hoseok": "j-hope",
    "taehyung": "v",
    "jungkook": "jungkook",
    "bulletproof": "bts",
    "hobi": "j-hope",
    "agust d": "suga"
}