import requests
import os
from dotenv import load_dotenv

# Load from .env if needed (though config.py usually handles this)
load_dotenv()

GEOAPIFY_API_KEY = os.getenv("GEOAPIFY_API_KEY", "29981c18c8e14cbc82c2a7e2f69d115f")

def geocode_place(place_name):
    """Get latitude and longitude for a place name."""
    try:
        url = f"https://api.geoapify.com/v1/geocode/search?text={place_name}&apiKey={GEOAPIFY_API_KEY}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if data["features"]:
                # Get first result
                lon, lat = data["features"][0]["geometry"]["coordinates"]
                return lat, lon
        return None, None
    except Exception as e:
        print(f"Geocoding error: {e}")
        return None, None

def get_nearby_places(lat, lon, categories="accommodation.hotel,catering.restaurant,tourism.attraction", radius=5000):
    """Fetch points of interest around coordinates."""
    try:
        url = f"https://api.geoapify.com/v2/places?categories={categories}&filter=circle:{lon},{lat},{radius}&limit=15&apiKey={GEOAPIFY_API_KEY}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            places = []
            for feature in data.get("features", []):
                props = feature.get("properties", {})
                name = props.get("name")
                if name:
                    address = props.get("address_line2", "")
                    cat_list = props.get("categories", [])
                    main_cat = cat_list[0] if cat_list else "place"
                    places.append(f"- {name} ({main_cat}): {address}")
            return places
        return []
    except Exception as e:
        print(f"Places API error: {e}")
        return []

def get_geoapify_data(place_name):
    """Combined function to get geocoded places."""
    lat, lon = geocode_place(place_name)
    if lat and lon:
        places = get_nearby_places(lat, lon)
        if places:
            return f"\nReal-world Locations in {place_name}:\n" + "\n".join(places)
    return ""
