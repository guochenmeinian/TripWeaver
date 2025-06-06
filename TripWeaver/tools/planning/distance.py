import os
from tarfile import data_filter
import requests
from dotenv import load_dotenv

load_dotenv()
GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAP_API_KEY")
print("GOOGLE_MAPS_API_KEY:", GOOGLE_MAPS_API_KEY)

def get_distance(origins: list[str], destinations: list[str], mode: str) -> dict:
    url = "https://maps.googleapis.com/maps/api/distancematrix/json"
    params = {
        "origins": "|".join(origins),
        "destinations": "|".join(destinations),
        "mode": mode,
        "key": GOOGLE_MAPS_API_KEY
    }

    response = requests.get(url, params=params)
    data = response.json()

    if data["status"] != "OK":
            return {"status": "error", "error_message": data.get("error_message", "Geocoding failed.")}
    
    distances_matrix = []
    for i, row in enumerate(data["rows"]):
        row_result = []
        for j, element in enumerate(row["elements"]):
            if element["status"] != "OK":
                row_result.append({"destination": destinations[j], "status": "error", "error_message": "Route unavailable"})
            else:
                row_result.append({
                    "destination": data["destination_addresses"][j],
                    "distance_m": element["distance"]["value"],
                    "distance_text": element["distance"]["text"],
                    "duration_s": element["duration"]["value"],
                    "duration_text": element["duration"]["text"],
                    "status": "success"
                })
        
        distances_matrix.append({
            "origin": data["origin_addresses"][i],
            "destinations": row_result
        })
    
    return {"status": "success", "mode": mode, "distances": distances_matrix}