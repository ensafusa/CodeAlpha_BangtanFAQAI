# test_vars.py
try:
    from config import GROQ_MODEL
    print(f"✅ Success! GROQ_MODEL is: {GROQ_MODEL}")
except ImportError:
    print("❌ Error: Could not find config.py")
except NameError:
    print("❌ Error: GROQ_MODEL is not inside config.py")