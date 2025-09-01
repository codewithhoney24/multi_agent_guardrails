# agents/weather_agent.py
# ---------------------------------------------------
# Weather Agent (can call Gemini to "phrase" an answer; guarded)
from guardrails.input_guard import check_input_guard
from guardrails.output_guard import check_output_guard
from tools.gemini_client import gemini_complete

class WeatherAgent:
    def handle(self, query: str) -> str:
        # Agent-level INPUT guard
        ok, why = check_input_guard(query)
        if not ok:
            return f"❌ Blocked: {why}."

        # --- Dummy weather data; Gemini used just to format nice text (optional) ---
        # Example: "Weather in Dubai"
        prompt = f"Write a one-line friendly weather update based on: '{query}'. If no temp given, say Sunny, 32°C."
        raw = gemini_complete(prompt)  # will fallback locally if API key missing
        response = raw or f"Weather: Sunny, Temp: 32°C for {query}"

        # Agent-level OUTPUT guard
        ok_out, why_out = check_output_guard(response)
        if not ok_out:
            return f"❌ Blocked: {why_out}."

        return response
