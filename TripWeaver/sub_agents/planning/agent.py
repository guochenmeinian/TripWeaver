import os
import requests
from dotenv import load_dotenv
from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool
from TripWeaver.sub_agents.planning import prompt
from TripWeaver.tools.planning.weather import weather_tool
from TripWeaver.tools.planning.geocoding import geolocation_tool
from TripWeaver.tools.planning.distance import distance_tool
from TripWeaver.tools.planning.place_info import place_full_info_tool
from TripWeaver.sub_agents.housing.agent import airbnb_agent
from TripWeaver.tools.planning.place_nearby import places_nearby_tool

housing_tool = AgentTool(agent=airbnb_agent)


planning_agent = Agent(
    name="planning_agent",
    model="gemini-2.0-flash",
    description="Generates travel itineraries based on user input and optionally checks weather.",
    instruction=prompt.PLANNING_AGENT_INSTR,
    tools=[
        weather_tool, 
        geolocation_tool, 
        distance_tool, 
        place_full_info_tool,
        places_nearby_tool,
        housing_tool],
   
)

