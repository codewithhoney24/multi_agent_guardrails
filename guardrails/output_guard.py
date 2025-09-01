# guardrails/output_guard.py
# ---------------------------------------------------
# Run-level and Agent-level OUTPUT guardrails
# Block U.S. cities in final responses

from typing import Tuple

US_CITIES = {
    "new york", "los angeles", "chicago", "houston", "phoenix",
    "philadelphia", "san antonio", "san diego", "dallas", "san jose",
    "austin", "jacksonville", "san francisco", "columbus", "fort worth",
    "indianapolis", "charlotte", "seattle", "denver", "washington",
    "boston", "usa", "united states"
}

def check_output_guard(output_text: str) -> Tuple[bool, str]:
    """Return (allowed, reason). If not allowed, reason explains why."""
    text = (output_text or "").lower()
    if any(city in text for city in US_CITIES):
        return False, "output references a restricted U.S. city"
    return True, ""
