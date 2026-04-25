def mode_agent(state: dict):
    """
    Mode Agent: Sets specific trip constraints based on the chosen mode.
    Modes: seasonal, short_trip, surprise
    """
    mode = state.get("mode", "seasonal")
    destination = state.get("destination", "")
    people_count = state.get("people_count", 1)
    
    constraints = f"Group Size: {people_count} {'person' if people_count == 1 else 'people'}. "
    
    # Surprise logic: pick a destination if empty
    if mode == "surprise" and (not destination or destination.lower() == "surprise me" or destination == "Random Destination"):
        import random
        popular = ["Paris", "Tokyo", "Bali", "New York", "Dubai", "Manali", "Goa", "Kerala", "Jaipur", "Rome", "London", "Sydney"]
        destination = random.choice(popular)
        state["destination"] = destination
        constraints += (
            f"SURPRISE DESTINATION: {destination}. "
            "The user doesn't know where they are going! Make it feel like a grand discovery. "
            "Include unique, off-beat, and 'hidden gem' locations. "
            "Avoid common tourist traps. Add one mysterious or unexpected activity per day."
        )
    elif mode == "short_trip":
        constraints += (
            "This is a HIGH-EFFICIENCY 'Power Trip'. The user wants to see the absolute BEST of the "
            "destination in a very limited time. Prioritize the top 3 globally iconic landmarks. "
            "Optimize for 'efficiency': group activities by neighborhood to minimize transit time. "
            "Suggest early starts and express transport options. Skip low-priority or time-consuming hidden gems."
        )
    elif mode == "seasonal":
        from datetime import datetime
        now = datetime.now()
        month_name = now.strftime("%B")
        # Simple season mapping (Northern Hemisphere focus, can be refined)
        month = now.month
        if month in [12, 1, 2]: season = "Winter"
        elif month in [3, 4, 5]: season = "Spring"
        elif month in [6, 7, 8]: season = "Summer"
        else: season = "Autumn"
        
        constraints += (
            f"This is a {season} SEASONAL vacation. Current Month: {month_name}. "
            f"Prioritize places and experiences that are best in {season}. "
            f"Suggest seasonal delicacies, festivals, and scenery specific to {month_name}. "
            "Ensure the pacing is relaxed and suitable for a holiday."
        )
    elif mode == "surprise":
         constraints += (
            "This is a SURPRISE trip. Include unique, off-beat, and 'hidden gem' locations. "
            "Avoid common tourist traps. Add one mysterious or unexpected activity per day."
        )
    else:
        constraints += "Standard balanced travel plan."

    state["constraints"] = constraints
    return state
