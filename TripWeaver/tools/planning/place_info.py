import os
import requests
from dotenv import load_dotenv
from google.adk.tools import FunctionTool

load_dotenv()
GOOGLE_MAPS_API_KEY = os.getenv("MAP_PLATFORM_API_KEY")


def get_place_full_info(place_name: str, location: str) -> dict:
    """
    Get Complete Place Information

    This tool retrieves detailed information about a specific place using the Google Places API.
    It is designed to support travel planning agents by providing rich metadata for places such as
    restaurants, landmarks, hotels, and attractions.

    Parameters:
    - place_name (str): The name of the place (e.g., "Tokyo Tower")
    - location (str): A broader location or city used to disambiguate the query (e.g., "Tokyo")

    Returns:
    A dictionary with the following keys (if successful):
    - status (str): "success" or "error"
    - place_name (str): Official name of the place
    - address (str): Formatted address
    - rating (float): Average user rating
    - total_reviews (int): Number of user reviews
    - summary (str): Editorial summary (if available)
    - opening_hours (List[str]): Opening hours by weekday
    - photo_reference (str): Reference ID for the primary photo
    - types (List[str]): Place types (e.g., "restaurant", "tourist_attraction")
    - website (str): Official website URL
    - google_maps_url (str): Direct link to Google Maps for the place
    - phone_number (str): International phone number
    - price_level (int): Price level (0 = free, 1–4 = increasing cost)

    Use this tool to:
    - Enhance travel suggestions with detailed place information
    - Filter places based on rating, type, or open hours
    - Display helpful context to users via UI or summary views
    """

    find_url = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json"
    find_params = {
        "input": f"{place_name} {location or ''}",
        "inputtype": "textquery",
        "fields": "place_id",
        "key": GOOGLE_MAPS_API_KEY
    }
    find_response = requests.get(find_url, params=find_params).json()
    candidates = find_response.get("candidates", [])
    if not candidates:
        return {"status": "error", "message": f"Place not found: {place_name}"}

    place_id = candidates[0]["place_id"]


    detail_url = "https://maps.googleapis.com/maps/api/place/details/json"
    detail_params = {
        "place_id": place_id,
        "fields": (
            "name,rating,user_ratings_total,formatted_address,"
            "editorial_summary,opening_hours,photos,types,"
            "website,url,international_phone_number,price_level"
        ),
        "key": GOOGLE_MAPS_API_KEY
    }
    detail_response = requests.get(detail_url, params=detail_params).json()
    result = detail_response.get("result", {})

    return {
        "status": "success",
        "place_name": result.get("name"),
        "address": result.get("formatted_address"),
        "rating": result.get("rating"),
        "total_reviews": result.get("user_ratings_total"),
        "summary": result.get("editorial_summary", {}).get("overview", "No summary available."),
        "opening_hours": result.get("opening_hours", {}).get("weekday_text", []),
        "photo_reference": result.get("photos", [{}])[0].get("photo_reference"),
        "types": result.get("types", []),
        "website": result.get("website"),
        "google_maps_url": result.get("url"),
        "phone_number": result.get("international_phone_number"),
        "price_level": result.get("price_level")
    }


place_full_info_tool = FunctionTool(get_place_full_info)



# import os
# import requests
# from dotenv import load_dotenv
# from google.adk.tools import FunctionTool

# load_dotenv()
# GOOGLE_MAPS_API_KEY = os.getenv("MAP_PLATFORM_API_KEY")

# def find_place_id(place_name: str, location: str = None) -> str:
#     find_url = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json"
#     params = {
#         "input": f"{place_name} {location or ''}",
#         "inputtype": "textquery",
#         "fields": "place_id",
#         "key": GOOGLE_MAPS_API_KEY
#     }
#     response = requests.get(find_url, params=params).json()

#     candidates = response.get("candidates", [])
#     if not candidates:
#         return None
#     return candidates[0]["place_id"]



# def get_place_opening_hours(place_name: str, location: str) -> dict:
#     """
#     Fetches the weekday opening hours of a given place using the Google Places API.

#     Parameters:
#     - place_name: The name of the place (e.g., 'British Museum')
#     - location: A broader location context to disambiguate (e.g., 'London')

#     Returns:
#     - A dictionary containing the official name and opening hours (Monday–Sunday)
#     - Status and error message if the place or hours cannot be retrieved

#     Useful for:
#     - Scheduling visits when places are open
#     - Avoiding closures or mistimed recommendations
#     """

#     place_id = find_place_id(place_name, location)
#     if not place_id:
#         return {"status": "error", "message": f"Place not found: {place_name}"}
    
#     detail_url = "https://maps.googleapis.com/maps/api/place/details/json"
#     params = {
#         "place_id": place_id,
#         "fields": "name,opening_hours",
#         "key": GOOGLE_MAPS_API_KEY
#     }
#     result = requests.get(detail_url, params=params).json().get("result", {})
    
#     if "opening_hours" in result:
#         return {
#             "status": "success",
#             "place_name": result["name"],
#             "opening_hours": result["opening_hours"].get("weekday_text", [])
#         }
#     else:
#         return {"status": "error", "message": "No opening hours available for this place."}



# def get_place_description(place_name: str, location: str) -> dict:
#     """
#     Retrieves basic information about a place using the Google Places API.

#     Parameters:
#     - place_name: The name of the place (e.g., 'Tower of London')
#     - location: A contextual location to refine the query (e.g., 'London')

#     Returns:
#     - A dictionary with place name, address, rating, total number of reviews,
#       and a brief editorial summary (if available)
#     - Includes error messages if the place cannot be found

#     Useful for:
#     - Writing rich, trustworthy descriptions of destinations
#     - Filtering out low-rated or poorly reviewed locations
#     """
#     place_id = find_place_id(place_name, location)
#     if not place_id:
#         return {"status": "error", "message": f"Place not found: {place_name}"}
    
#     detail_url = "https://maps.googleapis.com/maps/api/place/details/json"
#     params = {
#         "place_id": place_id,
#         "fields": "name,rating,user_ratings_total,formatted_address,editorial_summary",
#         "key": GOOGLE_MAPS_API_KEY
#     }
#     result = requests.get(detail_url, params=params).json().get("result", {})

#     return {
#         "status": "success",
#         "place_name": result.get("name"),
#         "address": result.get("formatted_address"),
#         "rating": result.get("rating"),
#         "total_reviews": result.get("user_ratings_total"),
#         "summary": result.get("editorial_summary", {}).get("overview", "No summary available.")
#     }

# place_open_hours_tool = FunctionTool(get_place_opening_hours)
# place_description_tool = FunctionTool(get_place_description)