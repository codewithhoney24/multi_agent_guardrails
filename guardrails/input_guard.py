# guardrails/input_guard.py
# ---------------------------------------------------
# Run-level and Agent-level INPUT guardrails
# 1) Block India-related city queries
# 2) Block unsafe content (e.g., hacking)

from typing import Tuple

INDIA_CITIES = {
    "delhi", "new delhi", "mumbai", "bombay", "bangalore", "bengaluru",
    "kolkata", "calcutta", "chennai", "hyderabad", "ahmedabad", "pune",
    "jaipur", "surat", "india"
}

UNSAFE_KEYWORDS = {
    "hack", "ddos", "sql injection", "xss", "exploit", "malware",
    "ransomware", "phishing", "crack server", "bypass login", "breach",
    "server attack", "botnet", "zero day"
}

def check_input_guard(user_input: str) -> Tuple[bool, str]:
    """Return (allowed, reason). If not allowed, reason holds the block reason."""
    q = (user_input or "").lower()

    # block clearly unsafe intent first
    if any(k in q for k in UNSAFE_KEYWORDS):
        return False, "unsafe content detected"

    # block india-related queries
    if any(city in q for city in INDIA_CITIES):
        return False, "india-related queries are not allowed"

    return True, ""
