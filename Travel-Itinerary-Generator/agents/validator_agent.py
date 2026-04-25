def validator_agent(state: dict):
    """Validator Agent: Multi-option aware."""
    plan = state.get("plan", {})
    options = plan.get("options", [])
    requested_days = state.get("days", 0)
    
    errors = []
    
    if not options:
        errors.append("No travel options were generated.")
    
    for i, opt in enumerate(options):
        itin = opt.get("itinerary", [])
        if len(itin) < requested_days:
            errors.append(f"{opt.get('option_id', f'Option {i+1}')} has only {len(itin)} days.")
        
        if not opt.get("hotel"):
            errors.append(f"{opt.get('option_id')} is missing hotel details.")

    if errors:
        plan["warning"] = " | ".join(errors)

    state["final_plan"] = plan
    return state
