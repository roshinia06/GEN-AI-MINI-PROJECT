def budget_agent(state: dict):
    """
    Budget Agent: Validates the generated plan against the budget and computes a
    detailed breakdown for the UI sidebar. Works with the morning/afternoon/evening schema.
    """
    plan = state.get("plan", {})
    budget = state.get("budget", 0)
    itinerary = plan.get("itinerary", [])
    people_count = state.get("people_count", 1)
    days = len(itinerary) or state.get("days", 1)

    # ── Collect costs from all time slots ─────────────────────────────
    accommodation_total = 0
    food_total = 0
    activities_total = 0

    for day in itinerary:
        # Sum activity costs from morning / afternoon / evening slots
        for slot in ("morning", "afternoon", "evening"):
            slot_data = day.get(slot, {})
            if isinstance(slot_data, dict):
                activities_total += slot_data.get("cost", 0)

        # Accommodation cost (support both 'accommodation' and legacy 'stay')
        acc = day.get("accommodation") or day.get("stay", {})
        if isinstance(acc, dict):
            accommodation_total += acc.get("cost_per_night", 0)

    # Food estimate: if the plan didn't include explicit costs, estimate from budget
    food_total = int(budget * 0.20)  # 20% of total budget for food

    # Recalculate total_cost from real slot costs if the AI's total_cost is 0 or missing
    ai_total = plan.get("total_cost", 0)
    if ai_total == 0:
        plan["total_cost"] = accommodation_total + activities_total + food_total

    total = plan["total_cost"]

    # ── Budget enforcement: scale down if over budget ──────────────────
    if total > budget and budget > 0:
        scale = budget / total
        for day in itinerary:
            for slot in ("morning", "afternoon", "evening"):
                slot_data = day.get(slot, {})
                if isinstance(slot_data, dict) and slot_data.get("cost"):
                    slot_data["cost"] = int(slot_data["cost"] * scale)
            acc = day.get("accommodation") or day.get("stay", {})
            if isinstance(acc, dict) and acc.get("cost_per_night"):
                acc["cost_per_night"] = int(acc["cost_per_night"] * scale)

        plan["total_cost"] = budget
        plan["warning"] = f"Costs adjusted to fit your budget of {budget} for {people_count} people."
        accommodation_total = int(accommodation_total * scale)
        activities_total = int(activities_total * scale)
        food_total = int(food_total * scale)
        total = budget

    # ── Build breakdown for the UI bars ───────────────────────────────
    buffer = int(total * 0.08)
    plan["budget_breakdown"] = {
        "flights": state.get("flight_cost_estimate", 0),
        "accommodation": accommodation_total,
        "food": food_total,
        "activities": activities_total,
        "buffer": buffer,
        "total": total,
    }

    plan["currency_symbol"] = state.get("currency_symbol", "₹")
    plan["people_count"] = people_count

    state["filtered_plan"] = plan
    return state
