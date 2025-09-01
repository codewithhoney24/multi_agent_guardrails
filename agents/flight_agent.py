# agents/flight_agent.py
# ---------------------------------------------------
# Flight Agent (dummy business logic + guardrails)
from guardrails.input_guard import check_input_guard
from guardrails.output_guard import check_output_guard

class FlightAgent:
    """Returns mock flight confirmations or listings."""

    def handle(self, query: str) -> str:
        # Agent-level INPUT guard
        ok, why = check_input_guard(query)
        if not ok:
            return f"❌ Blocked: {why}."

        # --- Dummy processing ---
        # In real life: call airline APIs etc.
        # We'll parse very lightly for demo:
        if "karachi" in query.lower() and "dubai" in query.lower():
            response = "Flight Confirmed: PK-213, Cost: $350"
        else:
            response = f"Flight results for: {query}"

        # Agent-level OUTPUT guard
        ok_out, why_out = check_output_guard(response)
        if not ok_out:
            return f"❌ Blocked: {why_out}."

        return response
