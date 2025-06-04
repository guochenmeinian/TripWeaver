import os
import requests
from dotenv import load_dotenv
from google.adk.agents import Agent
from TripWeaver.sub_agents.planning import prompt
from TripWeaver.tools.planning.weather import weather_tool
from TripWeaver.tools.planning.geocoding import geolocation_tool
from TripWeaver.tools.planning.distance import distance_tool
from TripWeaver.tools.planning.place_info import place_open_hours_tool, place_description_tool

planning_agent = Agent(
    name="planning_agent",
    model="gemini-2.0-flash",
    description="Generates travel itineraries based on user input and optionally checks weather.",
    instruction=prompt.PLANNING_AGENT_INSTR,
    tools=[weather_tool, geolocation_tool, distance_tool, place_open_hours_tool, place_description_tool],
)
