# config.py
import os
from dotenv import load_dotenv

# This looks for the .env file in your folder
load_dotenv()

# --- API KEYS ---
# It will now pull the key from your .env file automatically
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = "llama-3.3-70b-versatile"

# --- CONSOLE DEBUGGING ---
if GROQ_API_KEY:
    print(f"--- [SUCCESS] Groq API Key loaded (starts with: {GROQ_API_KEY[:6]}...) ---")
else:
    print("--- [ERROR] No API Key found! Check your .env file placement. ---")

# --- FILE PATHS ---
PDF_PATH = "Beyond-the-Story-_Retail_-3.pdf"

# --- AI PARAMETERS ---
CONTEXT_WINDOW = 3 # Kept small to avoid the 413 token error
SIMILARITY_THRESHOLD = 0.03

# --- K-POP DICTIONARY ---
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