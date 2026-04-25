import re
import json
import ollama
from config import MODEL_NAME
from utils.prompt_templates import PLANNER_PROMPT


def clean_json(text: str) -> str:
    """
    Extract and lightly clean a JSON object from raw LLM output.
    Only fixes the most common structural issues without corrupting valid JSON.
    """
    # Strip markdown code fences
    text = re.sub(r"```(?:json)?", "", text).strip()

    start = text.find("{")
    end = text.rfind("}") + 1
    if start == -1 or end == 0:
        return "{}"

    json_text = text[start:end]

    # Fix trailing commas before } or ]  (common LLM mistake)
    json_text = re.sub(r",\s*([}\]])", r"\1", json_text)

    return json_text


def build_fallback_plan(state: dict) -> dict:
    """
    Returns a valid placeholder plan matching the new Professional Travel Agency schema
    when the LLM output cannot be parsed.
    """
    destination = state.get("destination", "Your Destination")
    days = state.get("days", 1)
    budget = state.get("budget", 0)
    currency = state.get("currency_symbol", "₹")

    itinerary = []
    for d in range(1, days + 1):
        itinerary.append({
            "day": d,
            "title": f"{destination} Sightseeing & Exploration",
            "date": "TBD",
            "activities": [
                f"Pick up from the hotel and proceed towards {destination} landmarks.",
                f"Morning sightseeing includes historical spots and local centers.",
                f"Lunch at a highly-rated local restaurant.",
                f"After touring these locations, return to the hotel.",
                f"Overnight stay in {destination}."
            ],
            "city": destination,
            "meals": ["Breakfast", "Dinner"]
        })

    return {
        "destination": destination,
        "duration": f"{days} Days",
        "itinerary": itinerary,
        "total_cost": budget,
        "currency": currency,
        "tips": [
            "Carry local currency for small vendors",
            "Use local transport apps for best rates",
            "Book accommodations in advance for better deals",
        ],
        "warning": "AI response was malformed — showing a template plan. Try again for a detailed itinerary."
    }


def planner_agent(state: dict):
    """
    Planner Agent: Calls the LLM with a structured prompt and parses the JSON response.
    Falls back to a complete placeholder plan if parsing fails.
    """
    budget = state["budget"]
    days = state["days"]

    prompt = PLANNER_PROMPT.format(
        starting_place=state.get("starting_place", "Your location"),
        destination=state["destination"],
        budget=budget,
        days=days,
        context=state.get("context", ""),
        currency=state.get("currency_symbol", "₹"),
        mode=state.get("mode", "seasonal"),
        dietary=state.get("dietary_preference", "Both"),
    )

    try:
        response = ollama.chat(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": prompt}],
            options={"temperature": 0.7}
        )
        text = response["message"]["content"]
        
        cleaned = clean_json(text)
        parsed = json.loads(cleaned)

        # Ensure itinerary has exactly the requested number of days and correct structure
        existing = parsed.get("itinerary", [])
        while len(existing) < days:
            d = len(existing) + 1
            existing.append({
                "day": d,
                "title": f"Extended Exploration in {state['destination']}",
                "date": "TBD",
                "activities": ["Continue exploring local sights.", "Overnight stay."],
                "city": state['destination'],
                "meals": ["Breakfast"],
            })
        parsed["itinerary"] = existing[:days]

    except Exception as e:
        print(f"[planner_agent] Error: {e}. Using fallback plan.")
        parsed = build_fallback_plan(state)

    state["plan"] = parsed
    return state
