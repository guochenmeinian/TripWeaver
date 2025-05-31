import os
import requests
from dotenv import load_dotenv
from google.adk.agents import Agent
from TripWeaver.sub_agents.planning import prompt
from TripWeaver.tools.weather import get_weather_forecast
from TripWeaver.tools.geocoding import get_geolocation
from TripWeaver.tools.distance import get_distance

planning_agent = Agent(
    name="planning_agent",
    model="gemini-2.0-flash",
    description="Generates travel itineraries based on user input and optionally checks weather.",
    instruction=prompt.PLANNING_AGENT_INSTR,
    tools=[get_weather_forecast, get_geolocation, get_distance],
)
