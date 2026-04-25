import requests
import os

def get_flight_estimates(origin, destination):
    """
    Fetches indicative flight prices between origin and destination
    """
    api_key = os.getenv("RAPIDAPI_KEY")
    api_host = "booking-com15.p.rapidapi.com"
    
    if not api_key:
        return "Flight API key not configured."

    headers = {
        "X-RapidAPI-Key": api_key,
        "X-RapidAPI-Host": api_host
    }

    try:
        # Step 1: Search for airport codes
        def get_airport_code(query):
            url = f"https://{api_host}/api/v1/flights/searchDestination"
            res = requests.get(url, headers=headers, params={"query": query})
            data = res.json()
            if data.get("status") and data.get("data"):
                return data["data"][0].get("id") # Returns airport/city code
            return None

        origin_code = get_airport_code(origin)
        dest_code = get_airport_code(destination)

        if not origin_code or not dest_code:
            return f"Could not find airport codes for {origin} to {destination}"

        # Step 2: Get flight offers (simplified for context)
        url = f"https://{api_host}/api/v1/flights/searchFlights"
        params = {
            "fromId": origin_code,
            "toId": dest_code,
            "itineraryType": "ONE_WAY",
            "sortOrder": "PRICE",
            "currency_code": "USD"
        }
        
        res = requests.get(url, headers=headers, params=params)
        data = res.json()
        
        if not data.get("status") or not data.get("data"):
            return "No flight offers found for these locations."

        flights = data["data"].get("flightOffers", [])
        if not flights:
            return "No direct flights found."

        estimates = []
        for f in flights[:3]:
            price = f.get("price", {}).get("total", "N/A")
            airline = f.get("segments", [{}])[0].get("legs", [{}])[0].get("carrierName", "Local Airline")
            estimates.append(f"- {airline}: approx ${price} (One-way)")

        return "\n".join(estimates)

    except Exception as e:
        return f"Error fetching flight data: {str(e)}"
