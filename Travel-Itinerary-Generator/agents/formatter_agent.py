import json


def formatter_agent(state: dict) -> dict:
    """
    Formatter Agent: Normalizes multi-option Professional Travel Agency plans.
    """
    plan = state.get("plan", {})
    options = plan.get("options", [])
    
    # Ensure options have consistent fields
    formatted_options = []
    for opt in options:
        formatted_opt = {
            "option_id": opt.get("option_id", "Travel Option"),
            "hotel": opt.get("hotel", {}),
            "transport_facility": opt.get("transport_facility", "Private vehicle for transfers and sightseeing."),
            "itinerary": opt.get("itinerary", []),
            "pricing": opt.get("pricing", {"total_cost": 0, "per_person": 0})
        }
        formatted_options.append(formatted_opt)

    formatted = {
        "destination": plan.get("destination", state.get("destination", "")),
        "duration": plan.get("duration", f"{state.get('days', 0)} Days"),
        "options": formatted_options,
        "inclusions": plan.get("inclusions", []),
        "exclusions": plan.get("exclusions", []),
        "terms": plan.get("terms", []),
        "warning": plan.get("warning", ""),
        "currency_symbol": state.get("currency_symbol", "₹"),
    }

    state["final_plan"] = formatted
    return state
