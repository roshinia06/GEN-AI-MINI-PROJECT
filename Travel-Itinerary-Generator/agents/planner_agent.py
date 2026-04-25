import re
import json
import ollama
from config import MODEL_NAME
from utils.prompt_templates import PLANNER_PROMPT


def clean_json(text: str) -> str:
    """Extract and clean JSON from raw LLM output."""
    text = re.sub(r"```(?:json)?", "", text).strip()
    start = text.find("{")
    end = text.rfind("}") + 1
    if start == -1 or end == 0: return "{}"
    json_text = text[start:end]
    json_text = re.sub(r",\s*([}\]])", r"\1", json_text)
    return json_text


def build_fallback_plan(state: dict) -> dict:
    """Full fallback multi-option plan."""
    dest = state.get("destination", "Destination")
    days = state.get("days", 1)
    ppl = state.get("people_count", 1)
    nights = max(1, days - 1)

    options = []
    for opt_id, hotel, price in [("Option 1 (Budget)", "Eco Stay", 2000), ("Option 2 (Standard)", "Comfort Inn", 4500)]:
        itinerary = []
        for d in range(1, days + 1):
            itinerary.append({
                "day": d, "title": f"{dest} Discovery", "date": "TBD",
                "activities": [f"Pick up and proceed towards {dest}.", f"Explore local sights.", "Overnight stay."],
                "city": dest, "meals": ["Breakfast"]
            })
        
        total_cost = (price * nights) + (2000 * days)
        options.append({
            "option_id": opt_id,
            "hotel": {"name": hotel, "category": "3 Star", "room_type": "Standard", "price_per_night": price, "nights": nights},
            "itinerary": itinerary,
            "pricing": {"total_cost": total_cost, "per_person": total_cost // ppl}
        })

    return {
        "destination": dest, "duration": f"{days} Days",
        "options": options,
        "inclusions": ["Sightseeing", "Transfers", "Breakfast"],
        "exclusions": ["Flights", "Personal expenses"],
        "terms": ["Advance payment required"],
        "warning": "Template shown due to AI formatting error."
    }


def planner_agent(state: dict):
    """Planner Agent: Multi-option generation."""
    days = state.get("days", 1)
    nights = max(1, days - 1)
    
    prompt = PLANNER_PROMPT.format(
        starting_place=state.get("starting_place", "Your location"),
        destination=state["destination"],
        days=days,
        nights_count=nights,
        people_count=state.get("people_count", 1),
        context=state.get("context", ""),
        mode=state.get("mode", "seasonal"),
        dietary=state.get("dietary_preference", "Both"),
        constraints=state.get("constraints", ""),
    )

    try:
        response = ollama.chat(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": prompt}],
            options={"temperature": 0.7}
        )
        cleaned = clean_json(response["message"]["content"])
        parsed = json.loads(cleaned)

        # Basic validation: ensure options exist
        if not parsed.get("options"):
            raise ValueError("No options generated")

    except Exception as e:
        print(f"[planner_agent] Error: {e}. Falling back.")
        parsed = build_fallback_plan(state)

    state["plan"] = parsed
    return state
