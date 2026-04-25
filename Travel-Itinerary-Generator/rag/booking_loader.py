import requests
import os
from datetime import datetime, timedelta

def get_booking_hotels(city_name):
    """
    Fetches real hotel data from Booking.com via RapidAPI
    """
    api_key = os.getenv("RAPIDAPI_KEY")
    api_host = os.getenv("RAPIDAPI_HOST", "booking-com.p.rapidapi.com")
    
    if not api_key:
        return "Booking.com API key not configured."

    headers = {
        "X-RapidAPI-Key": api_key,
        "X-RapidAPI-Host": api_host
    }

    try:
        # 1. Get Destination ID
        loc_url = f"https://{api_host}/v1/hotels/locations"
        loc_params = {"name": city_name, "locale": "en-gb"}
        
        loc_res = requests.get(loc_url, headers=headers, params=loc_params)
        loc_data = loc_res.json()
        
        if not loc_data:
            return f"No destination found for {city_name}"
            
        dest_id = loc_data[0].get("dest_id")
        dest_type = loc_data[0].get("dest_type")

        # 2. Search Hotels (using dummy dates for context)
        checkin = (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d")
        checkout = (datetime.now() + timedelta(days=32)).strftime("%Y-%m-%d")
        
        search_url = f"https://{api_host}/v1/hotels/search"
        search_params = {
            "dest_id": dest_id,
            "dest_type": dest_type,
            "checkin_date": checkin,
            "checkout_date": checkout,
            "adults_number": "2",
            "room_number": "1",
            "order_by": "popularity",
            "units": "metric",
            "locale": "en-gb"
        }
        
        search_res = requests.get(search_url, headers=headers, params=search_params)
        search_data = search_res.json()
        
        results = search_data.get("result", [])
        if not results:
            return "No hotels found in this area."

        # Format top 5 hotels for context
        hotel_context = []
        for h in results[:5]:
            name = h.get("hotel_name")
            rating = h.get("review_score", "N/A")
            price = h.get("min_total_price", "N/A")
            currency = h.get("currency_code", "")
            address = h.get("address", "")
            
            hotel_context.append(f"- {name}: {rating}/10, ~{price} {currency} per night. Address: {address}")
            
        return "\n".join(hotel_context)

    except Exception as e:
        return f"Error fetching Booking.com data: {str(e)}"
