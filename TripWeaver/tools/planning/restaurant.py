import os
import requests
from dotenv import load_dotenv
from typing import List
from geocoding import get_geolocations
from concurrent.futures import ThreadPoolExecutor, as_completed

load_dotenv()
GOOGLE_MAPS_API_KEY = os.getenv("MAP_PLATFORM_API_KEY")
print("GOOGLE_MAPS_API_KEY:", GOOGLE_MAPS_API_KEY)

def get_restaurants_near_locations(addresses: List[str], radius: int = 500, keyword: str = "restaurant") -> List[dict]:
    geo_results = get_geolocations(addresses)
    all_restaurants = []

    def search_nearby_restaurants(lat: float, lng: float, location_name: str):
        url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
        params = {
            "location": f"{lat},{lng}",
            "radius": radius,
            "type": "restaurant",
            "keyword": keyword,
            "key": GOOGLE_MAPS_API_KEY
        }
        try:
            response = requests.get(url, params=params, timeout=5)
            data = response.json()
            if data.get("status") == "OK":
                for r in data.get("results", []):
                    all_restaurants.append({
                        "location_source": location_name,
                        "name": r.get("name"),
                        "address": r.get("vicinity"),
                        "rating": r.get("rating"),
                        "user_ratings_total": r.get("user_ratings_total"),
                        "place_id": r.get("place_id"),
                        "location": r.get("geometry", {}).get("location"),
                        "photo_reference": r.get("photos", [{}])[0].get("photo_reference"),
                    })
        except Exception as e:
            print(f"Error searching near {location_name}: {e}")

    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = []
        for result in geo_results:
            if result["status"] == "success":
                lat, lng = result["latitude"], result["longitude"]
                futures.append(executor.submit(search_nearby_restaurants, lat, lng, result["input"]))
                
        for future in as_completed(futures):
            future.result()

    return all_restaurants