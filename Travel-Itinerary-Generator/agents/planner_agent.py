import ollama
import json
from config import MODEL_NAME
from utils.prompt_templates import PLANNER_PROMPT


def clean_json(text):
    import re
    start = text.find("{")
    end = text.rfind("}") + 1
    if start == -1 or end == 0:
        return "{}"
    
    json_text = text[start:end]
    
    # Fix common JSON errors: add missing commas before closing brackets/braces
    # Use regex to handle various spacing patterns
    json_text = re.sub(r'(\])\s+(")', r'\1, \2', json_text)
    json_text = re.sub(r'(\})\s+(")', r'\1, \2', json_text)
    
    return json_text


def planner_agent(state: dict):

    budget = state["budget"]
    days = state["days"]
    budget_per_day = budget / days if days > 0 else budget

    prompt = PLANNER_PROMPT.format(
        starting_place=state.get("starting_place", "Your location"),
        destination=state["destination"],
        budget=budget,
        days=days,
        budget_per_day=int(budget_per_day),
        context=state.get("context", ""),
        currency=state.get("currency_symbol", "₹"),
        constraints=state.get("constraints", ""),
        mode=state.get("mode", "seasonal")
    )

    response = ollama.chat(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": prompt}]
    )

    text = response["message"]["content"]

    try:
        cleaned = clean_json(text)
        parsed = json.loads(cleaned)
    except Exception as e:
        # Fallback: create a basic structure if JSON parsing fails
        fallback_itinerary = []
        for d in range(1, days + 1):
            fallback_itinerary.append({
                "day": d,
                "morning": {"activity": "Explore City Center", "description": "Start your journey at the heart of the city.", "cost": 0},
                "afternoon": {"activity": "Local Sightseeing", "description": "Visit iconic landmarks.", "cost": 0},
                "evening": {"activity": "Evening Stroll", "description": "Enjoy the local atmosphere.", "cost": 0},
                "dining": "Recommended local restaurant",
                "accommodation": {"name": "Comfortable Hotel", "cost_per_night": 0}
            })

        parsed = {
            "destination": state.get("destination", ""),
            "duration": f"{days} days",
            "itinerary": fallback_itinerary,
            "total_cost": budget,
            "tips": ["Stay hydrated", "Use local transport"],
            "error": f"JSON parsing failed: {str(e)}"
        }

    state["plan"] = parsed
    return state
