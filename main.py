# main.py
# ---------------------------------------------------
# Two demos:
# 1) Secure Chat loop (blocks unsafe + india inputs; output guard)
# 2) AI Travel Assistant workflow (hotel -> flight -> weather)
#
# Run-level guardrails are enforced here before/after invoking agents.

from main_logger import get_logger
from guardrails.input_guard import check_input_guard
from guardrails.output_guard import check_output_guard
from agents.hotel_agent import HotelAgent
from agents.flight_agent import FlightAgent
from agents.weather_agent import WeatherAgent

logger = get_logger("app")

# Instantiate agents once
hotel_agent = HotelAgent()
flight_agent = FlightAgent()
weather_agent = WeatherAgent()

def run_travel_assistant(city_from: str, city_to: str):
    """Workflow-level orchestration with run-level guards at input+output."""

    user_text = f"Travel plan from {city_from} to {city_to}"
    # Run-level INPUT guard (before any agent runs)
    ok, why = check_input_guard(user_text)
    if not ok:
        logger.info(f"Run blocked by input guard: {why}")
        return f"❌ Run blocked: {why}."

    print("Welcome to AI Travel Assistant!")

    # HOTEL
    print(f"Fetching hotel details for {city_to}...")
    logger.info(f"Hotel details fetched for {city_to}")
    hotel_result = hotel_agent.handle(city_to)

    ok_out, why_out = check_output_guard(hotel_result)
    if not ok_out:
        return f"❌ Run blocked: {why_out}."
    print(hotel_result)

    # FLIGHT
    print(f"\nBooking flight from {city_from} to {city_to}...")
    logger.info(f"Flight booked from {city_from} to {city_to}")
    flight_result = flight_agent.handle(f"Flights from {city_from} to {city_to}")
    ok_out, why_out = check_output_guard(flight_result)
    if not ok_out:
        return f"❌ Run blocked: {why_out}."
    print(flight_result)

    # WEATHER
    print(f"\nFetching Weather in {city_to}...")
    weather_result = weather_agent.handle(f"Weather in {city_to}")
    ok_out, why_out = check_output_guard(weather_result)
    if not ok_out:
        return f"❌ Run blocked: {why_out}."
    print(weather_result)

    # Final thanks (run-level OUTPUT guard too)
    final_text = "\nThanks for using AI Travel Assistant!"
    ok_out, why_out = check_output_guard(final_text)
    if not ok_out:
        return f"❌ Run blocked: {why_out}."

    return final_text

def secure_chat_loop():
    """Interactive secure chat demo with logging & guardrails."""
    print("🤖 Secure AI Agent Started...")
    print("Type 'exit' to quit.\n")

    while True:
        user = input("You: ").strip()
        if user.lower() == "exit":
            print("👋 Goodbye!")
            logger.info("Session ended by user.")
            break

        # Run-level INPUT guard
        ok, why = check_input_guard(user)
        if not ok:
            print("❌ Input blocked by guardrails (unsafe content detected).")
            logger.info(f"Blocked unsafe input: {user}")
            continue

        logger.info("Input passed guardrails: %s", user)
        logger.info("User: %s", user)

        # For chat demo we simply greet; you can pipe to Gemini if you like
        ai_reply = "Hello! How can I assist you today?" if user.lower() in {"hi", "hello", "hey", "hello ai"} \
                   else "Got it. (Demo reply)"

        # Run-level OUTPUT guard
        ok_out, why_out = check_output_guard(ai_reply)
        if not ok_out:
            print("❌ Output blocked by guardrails.")
            continue

        print(f"AI: {ai_reply}")
        logger.info("AI: %s", ai_reply)

def demo_banner():
    print("\n==============================")
    print("1) Secure Chat Demo")
    print("2) Travel Assistant Demo (Karachi → Dubai)")
    print("3) Exit")
    print("==============================")

if __name__ == "__main__":
    # simple menu to reproduce both transcripts
    while True:
        demo_banner()
        choice = input("Select option (1/2/3): ").strip()
        if choice == "1":
            secure_chat_loop()
        elif choice == "2":
            result = run_travel_assistant("Karachi", "Dubai")
            print("\n" + result + "\n")
        elif choice == "3":
            print("Bye!")
            break
        else:
            print("Invalid choice.\n")
