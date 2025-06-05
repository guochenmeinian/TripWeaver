import os
import requests
from dotenv import load_dotenv
from typing import List, Optional
from TripWeaver.tools.planning.geocoding import get_geolocations
from concurrent.futures import ThreadPoolExecutor, as_completed
from google.adk.tools import FunctionTool, ToolContext
from TripWeaver.tools import memory

load_dotenv()
GOOGLE_MAPS_API_KEY = os.getenv("MAP_PLATFORM_API_KEY")

def get_places_near_locations(
    addresses: List[str],
    radius: int = 500,
    place_type: str = "restaurant", 
    keyword: Optional[str] = None,  
    tool_context: ToolContext = None
) -> List[dict]:
    """
    Finds nearby places (restaurants, hotels, attractions, etc.) around a list of addresses.

    Parameters:
    - addresses: A list of address strings (e.g., ["Shibuya, Tokyo"])
    - radius: Search radius in meters (default: 500)
    - place_type: Type of places to search for (e.g., 'restaurant', 'lodging', 'tourist_attraction')
    - keyword: Optional keyword for more specific filtering (e.g., 'sushi', 'capsule hotel')

    Returns:
    A list of dictionaries, each containing:
    - location_source: Original location provided by the user
    - name: Name of the place
    - address: Vicinity or address string
    - rating: User rating score
    - user_ratings_total: Number of user ratings
    - place_id: Unique place ID
    - location: Dictionary with latitude and longitude
    - photo_reference: Photo reference ID for static image retrieval
    - types: List of place types
    - google_maps_url: Direct URL to the place on Google Maps
    """
    geo_results = get_geolocations(addresses)
    all_results = []

    def search_nearby(lat: float, lng: float, location_name: str):
        url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
        params = {
            "location": f"{lat},{lng}",
            "radius": radius,
            "type": place_type,
            "key": GOOGLE_MAPS_API_KEY,
        }
        if keyword:
            params["keyword"] = keyword

        try:
            response = requests.get(url, params=params, timeout=5)
            data = response.json()
            if data.get("status") == "OK":
                for r in data.get("results", []):
                    all_results.append({
                        "location_source": location_name,
                        "name": r.get("name"),
                        "address": r.get("vicinity"),
                        "rating": r.get("rating"),
                        "user_ratings_total": r.get("user_ratings_total"),
                        "place_id": r.get("place_id"),
                        "location": r.get("geometry", {}).get("location"),
                        "photo_reference": r.get("photos", [{}])[0].get("photo_reference"),
                        "types": r.get("types", []),
                    })
        except Exception as e:
            print(f"Error searching near {location_name}: {e}")

    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [
            executor.submit(search_nearby, r["latitude"], r["longitude"], r["input"])
            for r in geo_results if r["status"] == "success"
        ]
        for future in as_completed(futures):
            future.result()

    if tool_context: 
        tool_context.state["planning_checklist"]["proximity_search_done"] = True
        memory.memorize("places_nearby", all_results, tool_context)

    return all_results

places_nearby_tool = FunctionTool(get_places_near_locations)