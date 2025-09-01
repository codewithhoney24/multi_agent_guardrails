# agents/hotel_agent.py
# ---------------------------------------------------
# Hotel Agent (uses a small tool for mock booking/search)
from guardrails.input_guard import check_input_guard
from guardrails.output_guard import check_output_guard
from tools.hotel_booking_tool import find_hotel

class HotelAgent:
    def handle(self, query: str) -> str:
        # Agent-level INPUT guard
        ok, why = check_input_guard(query)
        if not ok:
            return f"❌ Blocked: {why}."

        # --- Dummy processing using tool ---
        city = query
        hotel = find_hotel(city)
        response = f"Hotel Found: {hotel['name']}, Price: {hotel['price']} per night"

        # Agent-level OUTPUT guard
        ok_out, why_out = check_output_guard(response)
        if not ok_out:
            return f"❌ Blocked: {why_out}."

        return response
