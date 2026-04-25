def budget_agent(state: dict):
    """
    Budget Agent: Simplified for Professional Travel Agency schema.
    Computes a rule-of-thumb breakdown for the UI sidebar based on the total budget.
    """
    plan = state.get("plan", {})
    budget = state.get("budget", 0)
    people_count = state.get("people_count", 1)
    
    # In the new Professional schema, we often get a single total_cost from the LLM.
    # If not, we use the requested budget.
    total = int(plan.get("total_cost", budget))
    
    # Rule of thumb breakdown for UI bars
    breakdown = {
        "flights": state.get("flight_cost_estimate", 0),
        "accommodation": int(total * 0.40),
        "food": int(total * 0.25),
        "activities": int(total * 0.25),
        "buffer": int(total * 0.10),
        "total": total
    }
    
    plan["budget_breakdown"] = breakdown
    plan["currency_symbol"] = state.get("currency_symbol", "₹")
    plan["people_count"] = people_count
    
    # If AI estimated a cost significantly higher than budget, add a warning
    if total > budget and budget > 0:
        plan["warning"] = f"Note: This premium plan may slightly exceed your target budget. Estimated: {total}."

    state["filtered_plan"] = plan
    return state
