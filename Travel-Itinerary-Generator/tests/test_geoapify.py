import sys
import os

# Add the project directory to sys.path
sys.path.append(os.path.join(os.getcwd(), "Travel-Itinerary-Generator"))

from rag.geoapify_loader import get_geoapify_data

destination = "Jaipur"
print(f"--- Testing Geoapify Data Fetching for {destination} ---")
data = get_geoapify_data(destination)
if data:
    print(f"Data fetched successfully (length: {len(data)})")
    print(data)
else:
    print("Failed to fetch data or no places found.")
