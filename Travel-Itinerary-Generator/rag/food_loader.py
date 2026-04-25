import requests
import os

def get_food_recommendations(is_veg=True):
    """
    Fetches food recommendations from Sharanz Restaurant API
    """
    api_key = os.getenv("RAPIDAPI_KEY")
    api_host = "sharanz-restraunt-api.p.rapidapi.com"
    
    if not api_key:
        return "Food API key not configured."

    headers = {
        "X-RapidAPI-Key": api_key,
        "X-RapidAPI-Host": api_host
    }

    try:
        endpoint = "/food/veg" if is_veg else "/food/non-veg"
        url = f"https://{api_host}{endpoint}"
        
        res = requests.get(url, headers=headers)
        data = res.json()
        
        # Format the food list (assuming it returns a list or dict with food items)
        if isinstance(data, list):
            foods = [f.get("name", str(f)) for f in data[:10]]
            return ", ".join(foods)
        elif isinstance(data, dict):
            # Try to find a list in the dict
            for key in data:
                if isinstance(data[key], list):
                    foods = [f.get("name", str(f)) for f in data[key][:10]]
                    return ", ".join(foods)
        
        return str(data)[:200] # Fallback to raw string truncated

    except Exception as e:
        return f"Error fetching food data: {str(e)}"
