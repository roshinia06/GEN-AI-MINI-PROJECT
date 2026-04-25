def budget_agent(state: dict):
    """Budget Agent: Multi-option aware."""
    plan = state.get("plan", {})
    options = plan.get("options", [])
    
    # In multi-option mode, pricing is usually already calculated by the planner.
    # We just ensure every option has a valid breakdown for the UI if needed.
    for opt in options:
        total = opt.get("pricing", {}).get("total_cost", 0)
        opt["budget_breakdown"] = {
            "accommodation": int(total * 0.50),
            "food": int(total * 0.20),
            "activities": int(total * 0.20),
            "buffer": int(total * 0.10),
            "total": total
        }

    state["filtered_plan"] = plan
    return state
