import os
import requests
from dotenv import load_dotenv
from google.adk.agents import Agent
from TripWeaver.sub_agents.planning import prompt
from TripWeaver.tools.planning.weather import get_weather_forecast
from TripWeaver.tools.planning.geocoding import get_geolocations
from TripWeaver.tools.planning.distance import get_distance
from TripWeaver.tools.planning.place_info import get_place_opening_hours, get_place_description

planning_agent = Agent(
    name="planning_agent",
    model="gemini-2.0-flash",
    description="Generates travel itineraries based on user input and optionally checks weather.",
    instruction=prompt.PLANNING_AGENT_INSTR,
    tools=[get_weather_forecast, get_geolocations, get_distance, get_place_opening_hours, get_place_description],
)
