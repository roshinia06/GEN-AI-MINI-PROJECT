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
    Returns a valid placeholder plan matching the full schema
    when the LLM output cannot be parsed.
    """
    destination = state.get("destination", "Your Destination")
    days = state.get("days", 1)
    budget = state.get("budget", 0)
    budget_per_day = budget // days if days else budget

    itinerary = []
    for d in range(1, days + 1):
        itinerary.append({
            "day": d,
            "theme": f"Explore {destination}",
            "morning": {
                "activity": f"Morning walk around {destination} city center",
                "description": "Start your day exploring the heart of the destination.",
                "cost": int(budget_per_day * 0.2),
                "transport": "Walking"
            },
            "afternoon": {
                "activity": f"Visit top attractions in {destination}",
                "description": "Explore iconic local landmarks and cultural sites.",
                "cost": int(budget_per_day * 0.3),
                "transport": "Local taxi"
            },
            "evening": {
                "activity": f"Dinner and evening at {destination}",
                "description": "Experience local cuisine and evening atmosphere.",
                "cost": int(budget_per_day * 0.2),
                "transport": "Walking"
            },
            "dining": f"Local restaurant in {destination} — try the regional specialty",
            "accommodation": {
                "name": f"Comfortable hotel in {destination}",
                "cost_per_night": int(budget_per_day * 0.3)
            }
        })

    return {
        "destination": destination,
        "duration": f"{days} days",
        "itinerary": itinerary,
        "total_cost": budget,
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
    budget_per_day = budget // days if days > 0 else budget

    prompt = PLANNER_PROMPT.format(
        starting_place=state.get("starting_place", "Your location"),
        destination=state["destination"],
        budget=budget,
        days=days,
        budget_per_day=int(budget_per_day),
        context=state.get("context", ""),
        currency=state.get("currency_symbol", "₹"),
        constraints=state.get("constraints", ""),
        mode=state.get("mode", "seasonal"),
    )

    response = ollama.chat(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": prompt}],
        options={"temperature": 0.7}
    )

    text = response["message"]["content"]

    try:
        cleaned = clean_json(text)
        parsed = json.loads(cleaned)

        # Ensure itinerary has exactly the requested number of days
        existing = parsed.get("itinerary", [])
        while len(existing) < days:
            d = len(existing) + 1
            existing.append({
                "day": d,
                "theme": f"Day {d} in {state['destination']}",
                "morning": {"activity": "Morning exploration", "description": "Explore the local area.", "cost": 0, "transport": "Walking"},
                "afternoon": {"activity": "Afternoon sightseeing", "description": "Visit local landmarks.", "cost": 0, "transport": "Local taxi"},
                "evening": {"activity": "Evening leisure", "description": "Enjoy local food and culture.", "cost": 0, "transport": "Walking"},
                "dining": "Local restaurant recommendation",
                "accommodation": {"name": "Hotel (see day 1 for booking)", "cost_per_night": 0},
            })
        parsed["itinerary"] = existing[:days]  # cap to requested days

    except Exception as e:
        print(f"[planner_agent] JSON parse error: {e}. Using fallback plan.")
        parsed = build_fallback_plan(state)

    state["plan"] = parsed
    return state
