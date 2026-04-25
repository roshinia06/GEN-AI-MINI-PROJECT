import json

def formatter_agent(state: dict):
    """
    Formatter Agent: Ensures the final output is normalized and strictly follows the required schema.
    """
    # Use the best available plan
    plan = state.get("final_plan") or state.get("filtered_plan") or state.get("plan", {})
    
    # Ensure standard schema
    formatted = {
        "destination": str(plan.get("destination", state.get("destination", ""))),
        "duration": str(plan.get("duration", f"{state.get('days', 0)} days")),
        "itinerary": [],
        "total_cost": int(plan.get("total_cost", state.get("budget", 0))),
        "currency_symbol": str(state.get("currency_symbol", "₹")),
        "budget_breakdown": plan.get("budget_breakdown", {}),
        "tips": plan.get("tips", []),
        "warning": plan.get("warning", "")
    }
    
    raw_itinerary = plan.get("itinerary", [])
    for i, day in enumerate(raw_itinerary):
        formatted_day = {
            "day": int(day.get("day", i + 1)),
            "morning": day.get("morning", {}),
            "afternoon": day.get("afternoon", {}),
            "evening": day.get("evening", {}),
            "dining": day.get("dining", ""),
            "accommodation": day.get("accommodation", day.get("stay", {})),
            "currency_symbol": formatted["currency_symbol"]
        }
        formatted["itinerary"].append(formatted_day)
        
    state["final_plan"] = formatted
    return state
