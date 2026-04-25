import json


def formatter_agent(state: dict) -> dict:
    """
    Formatter Agent: Final normalization step.
    Ensures the output strictly follows the UI schema: morning/afternoon/evening slots.
    Merges data from 'filtered_plan' (budget-adjusted) or falls back to raw 'plan'.
    """
    # Use the most processed version available
    plan = state.get("filtered_plan") or state.get("plan", {})

    raw_itinerary = plan.get("itinerary", [])
    formatted_itinerary = []

    currency_symbol = state.get("currency_symbol", "₹")

    for i, day in enumerate(raw_itinerary):
        formatted_day = {
            "day": int(day.get("day", i + 1)),
            "theme": day.get("theme", ""),
            "morning": _normalize_slot(day.get("morning")),
            "afternoon": _normalize_slot(day.get("afternoon")),
            "evening": _normalize_slot(day.get("evening")),
            "dining": _normalize_dining(day.get("dining")),
            "accommodation": _normalize_accommodation(
                day.get("accommodation") or day.get("stay")
            ),
            "currency_symbol": currency_symbol,
        }
        formatted_itinerary.append(formatted_day)

    formatted = {
        "destination": str(plan.get("destination", state.get("destination", ""))),
        "duration": str(plan.get("duration", f"{state.get('days', 0)} days")),
        "mode": state.get("mode", "seasonal"),
        "starting_place": state.get("starting_place", ""),
        "itinerary": formatted_itinerary,
        "total_cost": int(plan.get("total_cost", state.get("budget", 0))),
        "currency_symbol": currency_symbol,
        "budget_breakdown": plan.get("budget_breakdown", {}),
        "tips": plan.get("tips", []),
        "warning": plan.get("warning", ""),
        "people_count": state.get("people_count", 1),
        "accommodation_type": state.get("accommodation_type", ""),
    }

    state["final_plan"] = formatted
    return state


# ── Helpers ────────────────────────────────────────────────────────────────

def _normalize_slot(slot) -> dict:
    """Ensures a time slot is a proper dict with required keys."""
    if not slot:
        return {}
    if isinstance(slot, str):
        return {"activity": slot, "description": "", "cost": 0, "transport": ""}
    if isinstance(slot, dict):
        return {
            "activity": slot.get("activity", ""),
            "description": slot.get("description", ""),
            "cost": int(slot.get("cost", 0)),
            "transport": slot.get("transport", ""),
        }
    return {}


def _normalize_dining(dining) -> str:
    """Ensures dining is a plain string."""
    if not dining:
        return ""
    if isinstance(dining, str):
        return dining
    if isinstance(dining, dict):
        return dining.get("recommendation") or dining.get("name") or json.dumps(dining)
    return str(dining)


def _normalize_accommodation(acc) -> dict:
    """Ensures accommodation is a proper dict."""
    if not acc:
        return {}
    if isinstance(acc, str):
        return {"name": acc, "cost_per_night": 0}
    if isinstance(acc, dict):
        return {
            "name": acc.get("name", ""),
            "cost_per_night": int(acc.get("cost_per_night", 0)),
        }
    return {}
