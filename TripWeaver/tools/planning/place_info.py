import os
import requests
from dotenv import load_dotenv

load_dotenv()
GOOGLE_MAPS_API_KEY = os.getenv("MAP_PLATFORM_API_KEY")

def find_place_id(place_name: str, location: str = None) -> str:
    find_url = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json"
    params = {
        "input": f"{place_name} {location or ''}",
        "inputtype": "textquery",
        "fields": "place_id",
        "key": GOOGLE_MAPS_API_KEY
    }
    response = requests.get(find_url, params=params).json()

    candidates = response.get("candidates", [])
    if not candidates:
        return None
    return candidates[0]["place_id"]


def get_place_opening_hours(place_name: str, location: str) -> dict:
    """
    Returns the opening hours of a specific place (if available).
    """
    place_id = find_place_id(place_name, location)
    if not place_id:
        return {"status": "error", "message": f"Place not found: {place_name}"}
    
    detail_url = "https://maps.googleapis.com/maps/api/place/details/json"
    params = {
        "place_id": place_id,
        "fields": "name,opening_hours",
        "key": GOOGLE_MAPS_API_KEY
    }
    result = requests.get(detail_url, params=params).json().get("result", {})
    
    if "opening_hours" in result:
        return {
            "status": "success",
            "place_name": result["name"],
            "opening_hours": result["opening_hours"].get("weekday_text", [])
        }
    else:
        return {"status": "error", "message": "No opening hours available for this place."}

def get_place_description(place_name: str, location: str) -> dict:
    """
    Returns basic details of a place such as name, address, rating, total reviews, and summary (if available).
    """
    place_id = find_place_id(place_name, location)
    if not place_id:
        return {"status": "error", "message": f"Place not found: {place_name}"}
    
    detail_url = "https://maps.googleapis.com/maps/api/place/details/json"
    params = {
        "place_id": place_id,
        "fields": "name,rating,user_ratings_total,formatted_address,editorial_summary",
        "key": GOOGLE_MAPS_API_KEY
    }
    result = requests.get(detail_url, params=params).json().get("result", {})

    return {
        "status": "success",
        "place_name": result.get("name"),
        "address": result.get("formatted_address"),
        "rating": result.get("rating"),
        "total_reviews": result.get("user_ratings_total"),
        "summary": result.get("editorial_summary", {}).get("overview", "No summary available.")
    }