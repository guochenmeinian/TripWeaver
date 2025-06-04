from datetime import datetime, timedelta
import os
import requests
from dotenv import load_dotenv
from collections import defaultdict
from google.adk.tools import FunctionTool  

load_dotenv()

def get_weather_forecast(city: str, start_date_str: str) -> dict:
    """Get a 5-day weather forecast (in 3-hour intervals) for a given city starting from a specific date.
    
    Useful for adjusting daily travel plans based on weather conditions like rain or sunshine.
    Perfect for travel planning, packing decisions, and outdoor activity scheduling.
    
    Parameters:
    - city: Name of the city (e.g., 'London', 'Paris', 'Tokyo')
    - start_date_str: Start date in YYYY-MM-DD format (e.g., '2025-06-15')
    
    Returns detailed weather information including temperature, conditions, and timing for each day.
    """
    url = "https://api.openweathermap.org/data/2.5/forecast"
    params = {"q": city, "appid": os.getenv("OPENWEATHER_API_KEY"), "units": "metric"}
    response = requests.get(url, params=params)
    data = response.json()

    forecasts = data.get("list", [])

    start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
    end_date = start_date + timedelta(days=5)

    daily_forecasts = defaultdict(list)
    for entry in forecasts:
        dt = datetime.strptime(entry["dt_txt"], "%Y-%m-%d %H:%M:%S")
        if start_date <= dt.date() < end_date:
            time = dt.strftime("%H:%M")
            desc = entry["weather"][0]["description"].capitalize()
            temp = entry["main"]["temp"]
            daily_forecasts[dt.date()].append(f"{time}: {desc}, {temp}°C")

    if not daily_forecasts:
        return {"status": "error", "error_message": f"No forecast found for {city} from {start_date_str}."}

    forecast_result = []
    for i in range(5):
        day = start_date + timedelta(days=i)
        if day in daily_forecasts:
            forecast_result.append({
                "date": day.strftime("%Y-%m-%d"),
                "details": daily_forecasts[day]
            })

    return {
        "status": "success",
        "city": city,
        "start_date": start_date_str,
        "forecast": forecast_result
    }

weather_tool = FunctionTool(get_weather_forecast)
