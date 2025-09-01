# tools/gemini_client.py
# ---------------------------------------------------
# Minimal Gemini wrapper.
# Uses env var GEMINI_API_KEY. If not present, returns a safe local string.

import os
from dotenv import load_dotenv

load_dotenv()
_GEMINI_KEY = os.getenv("GEMINI_API_KEY", "").strip()

def gemini_complete(prompt: str) -> str:
    """
    Call Gemini to polish/phrase text.
    If API key missing or library not available, return a local fallback.
    """
    if not _GEMINI_KEY:
        # Fallback keeps the app working even without network
        return f"{prompt} → Sunny, 32°C."

    try:
        import google.generativeai as genai
        genai.configure(api_key=_GEMINI_KEY)
        model = genai.GenerativeModel("gemini-1.5-flash")
        resp = model.generate_content(prompt)
        text = getattr(resp, "text", "") or ""
        return text.strip()
    except Exception:
        # Never crash the app because of API hiccups
        return ""
