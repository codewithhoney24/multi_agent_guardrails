# tools/hotel_booking_tool.py
# ---------------------------------------------------
# Simple mock tool that "finds" a hotel for a city.

def find_hotel(city: str) -> dict:
    city_l = (city or "").lower()
    if "dubai" in city_l:
        return {"name": "Atlantis The Palm", "price": "$500"}
    if "istanbul" in city_l:
        return {"name": "Sura Hagia Sophia", "price": "$180"}
    # default
    return {"name": "City Center Hotel", "price": "$120"}
