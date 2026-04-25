from rag.wiki_loader import get_wiki_data
from rag.processor import process_text
from rag.vector_store import add_to_vector_store, query_vector_store
from rag.geoapify_loader import get_geoapify_data
from rag.booking_loader import get_booking_hotels
from rag.flight_loader import get_flight_estimates
from rag.food_loader import get_food_recommendations


def retrieval_agent(state: dict):
    destination = state["destination"]
    origin = state.get("starting_place", "Your location")
    notes = state.get("notes", "").lower()
    is_veg = "veg" in notes or "vegetarian" in notes

    # 1. Get wiki data
    wiki_raw = get_wiki_data(destination)
    
    # 2. Process it
    wiki_processed = process_text(wiki_raw, destination)

    # 3. Add to vector DB
    add_to_vector_store([wiki_processed])

    # 4. Get vector DB data
    rag_results = query_vector_store(destination)
    rag_data = ""
    if rag_results and len(rag_results) > 0:
        rag_data = "\n".join(rag_results[0])
    
    # 5. Get Geoapify data
    geo_data = get_geoapify_data(destination)
    
    # 6. Get real Booking.com hotels
    hotel_data = get_booking_hotels(destination)
    
    # 7. Get Flight estimates
    flight_data = get_flight_estimates(origin, destination)
    
    # 8. Get Food suggestions
    food_data = get_food_recommendations(is_veg=is_veg)

    context = (
        f"## GEOGRAPHIC & CULTURAL CONTEXT\n{wiki_processed}\n\n"
        f"## POPULAR ATTRACTIONS & PLACES\n{geo_data}\n\n"
        f"## RECOMMENDED REAL HOTELS (Booking.com)\n{hotel_data}\n\n"
        f"## FLIGHT ESTIMATES FROM {origin.upper()}\n{flight_data}\n\n"
        f"## RECOMMENDED {'VEGETARIAN' if is_veg else 'LOCAL'} DISHES\n{food_data}\n\n"
        f"## DETAILED LOCAL INSIGHTS (RAG)\n{rag_data}"
    )

    state["context"] = context
    return state
