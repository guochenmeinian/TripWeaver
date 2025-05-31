import os
import requests
from dotenv import load_dotenv

load_dotenv()
GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAP_API_KEY")
print("GOOGLE_MAPS_API_KEY:", GOOGLE_MAPS_API_KEY)


def get_geolocation(address: str) -> dict:
    try:
        url = "https://maps.googleapis.com/maps/api/geocode/json"
        params = {
            "address": address,
            "key": GOOGLE_MAPS_API_KEY
        }

        response = requests.get(url, params=params)
        data = response.json()

        if data["status"] != "OK":
            return {"status": "error", "error_message": data.get("error_message", "Geocoding failed.")}

        result = data["results"][0]
        location = result["geometry"]["location"]
        return {
            "status": "success",
            "address": result["formatted_address"],
            "latitude": location["lat"],
            "longitude": location["lng"]
        }

    except Exception as e:
        return {"status": "error", "error_message": str(e)}