def validator_agent(state: dict):
    plan = state.get("filtered_plan", {})
    itinerary = plan.get("itinerary", [])
    requested_days = state.get("days", 0)
    
    errors = []
    
    # 1. Check day count
    if len(itinerary) < requested_days:
        errors.append(f"Itinerary has only {len(itinerary)} days, but {requested_days} were requested.")
    
    # 2. Check for empty activities
    for i, day in enumerate(itinerary):
        if not day.get("activities"):
            errors.append(f"Day {i+1} has no activities.")
        if not day.get("stay"):
            errors.append(f"Day {i+1} is missing accommodation.")

    if errors:
        plan["warning"] = " | ".join(errors)
        state["validation_errors"] = errors

    state["final_plan"] = plan
    return state
