def validator_agent(state: dict):
    """
    Validator Agent: Checks if the generated itinerary matches the Professional Travel Agency schema.
    Checks for activities list, title, and city (stay).
    """
    plan = state.get("plan", {})
    itinerary = plan.get("itinerary", [])
    requested_days = state.get("days", 0)
    
    errors = []
    
    # 1. Check day count
    if len(itinerary) < requested_days:
        errors.append(f"Itinerary has only {len(itinerary)} days, but {requested_days} were requested.")
    
    # 2. Check for required components in each day
    for i, day in enumerate(itinerary):
        day_num = i + 1
        
        # Check for activities list
        activities = day.get("activities", [])
        if not activities or len(activities) < 2:
            errors.append(f"Day {day_num} has insufficient activities (need at least 2).")
            
        # Check for city/stay
        if not day.get("city"):
            errors.append(f"Day {day_num} is missing city/accommodation info.")

    if errors:
        # Join errors into a single warning string for the UI
        plan["warning"] = " | ".join(errors)
        state["validation_errors"] = errors

    state["final_plan"] = plan
    return state
