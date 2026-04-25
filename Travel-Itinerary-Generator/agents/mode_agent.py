import random
from datetime import datetime


SURPRISE_DESTINATIONS = [
    "Paris", "Tokyo", "Bali", "New York", "Dubai", "Manali",
    "Goa", "Kerala", "Jaipur", "Rome", "London", "Sydney",
    "Barcelona", "Maldives", "Istanbul", "Prague", "Santorini",
    "Kyoto", "Singapore", "Amsterdam",
]


def mode_agent(state: dict):
    """
    Mode Agent: Sets specific trip constraints based on the chosen mode.
    Modes: seasonal | short_trip | surprise
    """
    mode = state.get("mode", "seasonal")
    destination = state.get("destination", "")
    people_count = state.get("people_count", 1)
    interests = state.get("interests", [])
    accommodation_type = state.get("accommodation_type", "Mid-range")
    notes = state.get("notes", "")

    # Build base constraints
    constraints = f"Group Size: {people_count} {'person' if people_count == 1 else 'people'}. "
    constraints += f"Accommodation Preference: {accommodation_type}. "
    constraints += f"Dietary Preference: {state.get('dietary_preference', 'Both')}. "

    if interests:
        constraints += f"Interests: {', '.join(interests)}. "

    if notes:
        constraints += f"Special Notes: {notes}. "

    # ── SURPRISE MODE ──────────────────────────────────────────────────
    if mode == "surprise":
        # Pick a random destination if none specified (or it's a placeholder)
        if not destination or destination.lower() in ("", "random destination", "surprise me"):
            destination = random.choice(SURPRISE_DESTINATIONS)
            state["destination"] = destination

        constraints += (
            f"SURPRISE DESTINATION: {destination}. "
            "The user does NOT know where they are going — make the reveal feel grand! "
            "Include unique, off-beat, and 'hidden gem' locations. "
            "Avoid common tourist traps. "
            "Add at least one mysterious or unexpected activity per day. "
            "Open Day 1 with a sense of wonder and discovery."
        )

    # ── SHORT TRIP / POWER TRIP MODE ───────────────────────────────────
    elif mode == "short_trip":
        constraints += (
            "This is a HIGH-EFFICIENCY 'Power Trip'. The user wants to see the absolute BEST of the "
            "destination in minimal time. Prioritize the top 3 globally iconic landmarks. "
            "Group activities by neighbourhood to minimize transit time. "
            "Suggest early starts and express transport options. "
            "Skip low-priority or time-consuming activities."
        )

    # ── SEASONAL MODE ──────────────────────────────────────────────────
    elif mode == "seasonal":
        now = datetime.now()
        month_name = now.strftime("%B")
        month = now.month

        if month in (12, 1, 2):
            season = "Winter"
        elif month in (3, 4, 5):
            season = "Spring"
        elif month in (6, 7, 8):
            season = "Summer"
        else:
            season = "Autumn"

        constraints += (
            f"This is a {season} SEASONAL vacation. Current Month: {month_name}. "
            f"Recommend places and experiences that are BEST in {season}. "
            f"Suggest seasonal delicacies, local festivals, and scenery specific to {month_name}. "
            "Keep the pace relaxed and holiday-appropriate."
        )

    else:
        constraints += "Standard balanced travel plan."

    state["constraints"] = constraints
    return state
