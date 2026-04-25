import os
import requests
import wikipedia
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from config import GEOAPIFY_API_KEY


def geoapify_to_text(place):
    """Structures raw Geoapify data into readable context."""
    p = place.get("properties", {})
    categories = p.get('categories', [])
    category_str = ", ".join(categories) if isinstance(categories, list) else str(categories)
    
    return f"""
    Name: {p.get('name', 'N/A')}
    Category: {category_str}
    Address: {p.get('formatted', 'N/A')}
    Type: {'Hotel' if 'hotel' in category_str.lower() else 'Attraction/Restaurant'}
    Rating: {p.get('rating', 'N/A')}
    """


def retrieval_agent(state: dict):
    """
    Retrieval Agent: Combines Wikipedia, Geoapify, and RAG.
    Now structured for better context embedding.
    """
    destination = state["destination"]
    dietary = state.get("dietary_preference", "Both")
    
    # 1. Wikipedia Search
    try:
        wiki_data = wikipedia.summary(f"{destination} tourism", sentences=5)
    except:
        wiki_data = f"Information about {destination}."

    # 2. Geoapify (Hotels & Attractions)
    geo_context = []
    try:
        # Search for POIs
        url = f"https://api.geoapify.com/v2/places?categories=tourism,entertainment,leisure,catering&filter=rect:-180,-90,180,90&limit=20&apiKey={GEOAPIFY_API_KEY}"
        # Note: In a real app, we would use proper lat/lon geocoding for the destination.
        # For now, we simulate the structure improvement requested.
        resp = requests.get(url).json()
        for feature in resp.get("features", []):
            geo_context.append(geoapify_to_text(feature))
    except Exception as e:
        print(f"[retrieval] Geoapify error: {e}")

    # 3. Combine Sources
    combined_context = f"WIKIPEDIA SUMMARY:\n{wiki_data}\n\nLOCAL INTELLIGENCE (Geoapify):\n" + "\n".join(geo_context[:10])
    
    # 4. Optional: RAG from Vector Store (if exists)
    try:
        from datetime import datetime
        now = datetime.now()
        month = now.month
        season = "Winter" if month in (12, 1, 2) else "Spring" if month in (3, 4, 5) else "Summer" if month in (6, 7, 8) else "Autumn"
        
        embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        db = Chroma(persist_directory="./chroma_db", embedding_function=embeddings)
        
        search_query = f"{destination} hotels restaurants tourist attractions itinerary {dietary}"
        if state.get("mode") == "seasonal":
            search_query += f" best things to do in {season} {now.strftime('%B')} festivals delicacies"
            
        docs = db.similarity_search(search_query, k=3)
        rag_context = "\n".join([d.page_content for d in docs])
        combined_context += f"\n\nCURATED SEASONAL DATA:\n{rag_context}"
    except:
        pass

    state["context"] = combined_context
    return state
