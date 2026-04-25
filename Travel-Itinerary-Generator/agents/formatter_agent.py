import json


def formatter_agent(state: dict) -> dict:
    """
    Formatter Agent: Final normalization step for Professional Travel Agency style.
    Ensures the output follows the new activities-list schema.
    """
    plan = state.get("plan", {})
    raw_itinerary = plan.get("itinerary", [])
    formatted_itinerary = []

    currency_symbol = state.get("currency_symbol", "₹")

    for i, day in enumerate(raw_itinerary):
        formatted_day = {
            "day": int(day.get("day", i + 1)),
            "title": day.get("title", f"Day {i+1} Sightseeing"),
            "date": day.get("date", ""),
            "activities": _normalize_activities(day.get("activities")),
            "city": day.get("city", state.get("destination", "")),
            "meals": day.get("meals", []),
            "currency_symbol": currency_symbol,
        }
        formatted_itinerary.append(formatted_day)

    formatted = {
        "destination": str(plan.get("destination", state.get("destination", ""))),
        "duration": str(plan.get("duration", f"{state.get('days', 0)} Days")),
        "mode": state.get("mode", "seasonal"),
        "starting_place": state.get("starting_place", ""),
        "itinerary": formatted_itinerary,
        "total_cost": int(plan.get("total_cost", state.get("budget", 0))),
        "currency_symbol": currency_symbol,
        "budget_breakdown": plan.get("budget_breakdown", {}),
        "tips": plan.get("tips", []),
        "warning": plan.get("warning", ""),
        "people_count": state.get("people_count", 1),
    }

    state["final_plan"] = formatted
    return state


def _normalize_activities(activities) -> list:
    """Ensures activities is a list of strings."""
    if not activities:
        return []
    if isinstance(activities, list):
        return [str(a) for a in activities]
    if isinstance(activities, str):
        return [activities]
    if isinstance(activities, dict):
        # Fallback for old schema if it somehow appears
        acts = []
        for slot in ["morning", "afternoon", "evening"]:
            if slot in activities:
                s = activities[slot]
                if isinstance(s, dict):
                    acts.append(s.get("activity", ""))
                else:
                    acts.append(str(s))
        return [a for a in acts if a]
    return []
