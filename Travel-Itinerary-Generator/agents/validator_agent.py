def validator_agent(state: dict):
    """
    Validator Agent: Checks if the generated itinerary matches the requested constraints
    and has all required components in the new morning/afternoon/evening schema.
    """
    # Use filtered_plan if available (from budget agent), otherwise raw plan
    plan = state.get("filtered_plan") or state.get("plan", {})
    itinerary = plan.get("itinerary", [])
    requested_days = state.get("days", 0)
    
    errors = []
    
    # 1. Check day count
    if len(itinerary) < requested_days:
        errors.append(f"Itinerary has only {len(itinerary)} days, but {requested_days} were requested.")
    
    # 2. Check for required components in each day
    for i, day in enumerate(itinerary):
        day_num = i + 1
        
        # Check for activities (at least one of morning/afternoon/evening should be present)
        has_activity = any([
            day.get("morning"),
            day.get("afternoon"),
            day.get("evening")
        ])
        if not has_activity:
            errors.append(f"Day {day_num} has no activities.")
            
        # Check for accommodation (stay)
        if not day.get("accommodation") and not day.get("stay"):
            errors.append(f"Day {day_num} is missing accommodation.")

    if errors:
        # Join errors into a single warning string for the UI
        plan["warning"] = " | ".join(errors)
        state["validation_errors"] = errors

    state["final_plan"] = plan
    return state
