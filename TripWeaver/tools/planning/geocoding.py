import os
import time
import requests
from typing import List
from dotenv import load_dotenv
from concurrent.futures import ThreadPoolExecutor, as_completed
from google.adk.tools import FunctionTool


load_dotenv()
GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAP_API_KEY")


def get_geolocations(addresses: List[str]) -> List[dict]:
    """
    Convert a list of address strings into geographic coordinates (latitude and longitude).

    Parameters:
    - addresses: A list of human-readable location strings (e.g., ['Empire State Building, NY'])

    Returns:
    - A list of dictionaries containing:
      - formatted address
      - latitude and longitude
      - status and optional error messages for each input address

    Useful for:
    - Mapping
    - Distance estimation
    - Weather lookup by coordinates
    """
    results = []

    def geocode_job(address: str) -> dict:
        url = "https://maps.googleapis.com/maps/api/geocode/json"
        params = {"address": address, "key": GOOGLE_MAPS_API_KEY}
        retries = 3

        for attempt in range(retries):
            try:
                response = requests.get(url, params=params, timeout=5)
                data = response.json()

                if data["status"] == "OK":
                    result = data["results"][0]
                    location = result["geometry"]["location"]
                    return {
                        "status": "success",
                        "input": address,
                        "address": result["formatted_address"],
                        "latitude": location["lat"],
                        "longitude": location["lng"]
                    }

                elif data["status"] in {"OVER_QUERY_LIMIT", "UNKNOWN_ERROR"}:
                    time.sleep(2 ** attempt)
                else:
                    return {
                        "status": "error",
                        "input": address,
                        "error_message": data.get("error_message", data["status"])
                    }

            except Exception as e:
                if attempt == retries - 1:
                    return {"status": "error", "input": address, "error_message": str(e)}
                time.sleep(2 ** attempt)

        return {"status": "error", "input": address, "error_message": "Failed after retries"}

    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = {executor.submit(geocode_job, addr): addr for addr in addresses}
        for future in as_completed(futures):
            results.append(future.result())

    return results

geolocation_tool = FunctionTool(get_geolocations)