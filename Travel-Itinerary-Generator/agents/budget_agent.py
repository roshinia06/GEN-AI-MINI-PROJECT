def budget_agent(state: dict):
    plan = state["plan"]
    budget = state["budget"]
    itinerary = plan.get("itinerary", [])
    people_count = state.get("people_count", 1)
    
    accommodation_total = 0
    food_total = 0
    activities_total = 0
    
    # Analyze and adjust if over budget
    if plan.get("total_cost", 0) > budget:
        # Sort days by cost to find expensive ones
        sorted_days = sorted(itinerary, key=lambda x: x.get("estimated_cost", 0), reverse=True)
        
        # Heuristic: swap expensive stay for a more modest one if over budget
        for day in sorted_days:
            if plan["total_cost"] > budget:
                orig_cost = day.get("estimated_cost", 0)
                # Reduce stay cost by 30% as a 'swap'
                stay = day.get("stay", {})
                if isinstance(stay, dict) and stay.get("cost_per_night", 0) > 0:
                    reduction = stay["cost_per_night"] * 0.3
                    stay["cost_per_night"] -= int(reduction)
                    day["estimated_cost"] -= int(reduction)
                    plan["total_cost"] -= int(reduction)
                    plan["warning"] = f"Adjusted some stays to fit budget for {people_count} people."

    # Recalculate totals for breakdown
    for day in itinerary:
        cost = day.get("estimated_cost", 0)
        # Simplified breakdown for UI bars
        accommodation_total += cost * 0.45
        food_total += cost * 0.25
        activities_total += cost * 0.30

    plan["budget_breakdown"] = {
        "flights": 0,
        "accommodation": int(accommodation_total),
        "food": int(food_total),
        "activities": int(activities_total),
        "buffer": int(plan["total_cost"] * 0.1),
        "total": plan["total_cost"]
    }
    
    plan["currency_symbol"] = state.get("currency_symbol", "₹")
    plan["people_count"] = people_count
    
    state["filtered_plan"] = plan
    return state
