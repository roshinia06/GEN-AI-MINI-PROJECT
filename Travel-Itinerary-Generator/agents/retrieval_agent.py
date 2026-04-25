from rag.wiki_loader import get_wiki_data
from rag.processor import process_text
from rag.vector_store import add_to_vector_store, query_vector_store
from rag.geoapify_loader import get_geoapify_data
from rag.booking_loader import get_booking_hotels
from rag.flight_loader import get_flight_estimates
from rag.food_loader import get_food_recommendations


def retrieval_agent(state: dict) -> dict:
    """
    Retrieval Agent: Gathers multi-source context for the Planner Agent.
    Sources: Wikipedia, Geoapify (POI), Booking.com hotels, Flights, Food API, Vector DB.
    """
    destination = state["destination"]
    origin = state.get("starting_place", "Your location")
    notes = state.get("notes", "").lower()
    interests = state.get("interests", [])

    dietary = state.get("dietary_preference", "Both").lower()
    
    # Detect dietary preference
    is_veg = dietary == "veg" or "veg" in notes or "vegetarian" in notes
    is_both = dietary == "both"
    
    food_label = "VEGETARIAN" if is_veg else "LOCAL NON-VEG"
    if is_both:
        food_label = "VEGETARIAN & LOCAL NON-VEG"

    # 1. Wikipedia data → process → add to vector DB
    wiki_raw = get_wiki_data(destination)
    wiki_processed = process_text(wiki_raw, destination)
    add_to_vector_store([wiki_processed])

    # 2. Query vector DB for relevant snippets
    rag_results = query_vector_store(destination)
    rag_data = "\n".join(rag_results[0]) if rag_results and rag_results[0] else ""

    # 3. Geoapify POI data
    geo_data = get_geoapify_data(destination)

    # 4. Booking.com hotels
    hotel_data = get_booking_hotels(destination)

    # 5. Flight estimates
    flight_data = get_flight_estimates(origin, destination)

    # 6. Food suggestions (veg or non-veg)
    food_data = get_food_recommendations(is_veg=is_veg)

    # Assemble rich context block for the planner
    context = (
        f"## GEOGRAPHIC & CULTURAL CONTEXT\n{wiki_processed}\n\n"
        f"## POPULAR ATTRACTIONS & PLACES (Live Data)\n{geo_data}\n\n"
        f"## RECOMMENDED HOTELS (Booking.com)\n{hotel_data}\n\n"
        f"## FLIGHT ESTIMATES FROM {origin.upper()}\n{flight_data}\n\n"
        f"## {food_label} FOOD RECOMMENDATIONS\n{food_data}\n\n"
        f"## ADDITIONAL LOCAL INSIGHTS (RAG)\n{rag_data}"
    )

    state["context"] = context
    return state
