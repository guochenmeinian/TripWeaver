"""Inspiration agent. A pre-booking agent covering the ideation part of the trip."""

from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool
# You might also need FunctionTool if map_tool is a FunctionTool directly
# from google.adk.tools import FunctionTool 

from TripWeaver.shared_libraries.types import GeminiSpotSuggestions, POISuggestions, json_response_config
from TripWeaver.sub_agents.inspiration import prompt
from TripWeaver.tools.places import map_tool
# Assuming weather_tool here refers to the FunctionTool created from get_weather_forecast
# If weather_tool is defined as a FunctionTool instance in weather.py, that's fine.
# If it's the raw get_weather_forecast function, you'd need FunctionTool(weather_tool) for weather_agent's tools.
from TripWeaver.tools.planning.weather import weather_tool 

# Define weather_agent
weather_agent = Agent(
    model="gemini-2.0-flash",
    name="weather_agent",
    description="This agent provides weather information given a place",
    instruction=prompt.WEATHER_AGENT_INSTR,
    disallow_transfer_to_parent=True,
    disallow_transfer_to_peers=True,
    # IMPORTANT: weather_agent itself needs its own tools. If weather_tool is just a function,
    # it needs to be wrapped here in FunctionTool.
    # If weather_tool is already a FunctionTool instance, then tools=[weather_tool] is correct for this agent.
    tools=[weather_tool] # Assuming weather_tool is already a FunctionTool instance (e.g. from weather.py)
)

# Define place_agent
place_agent = Agent(
    model="gemini-2.0-flash",
    name="place_agent",
    instruction=prompt.PLACE_AGENT_INSTR,
    description="This agent suggests a few destination given some user preferences",
    disallow_transfer_to_parent=True,
    disallow_transfer_to_peers=True,
    output_schema=GeminiSpotSuggestions,
    output_key="place_suggestions",
    generate_content_config=json_response_config,
)

# Define poi_agent
poi_agent = Agent(
    model="gemini-2.0-flash",
    name="poi_agent",
    description="This agent suggests a few activities and points of interests given a destination",
    instruction=prompt.POI_AGENT_INSTR,
    disallow_transfer_to_parent=True,
    disallow_transfer_to_peers=True,
    output_schema=POISuggestions,
    output_key="poi_suggestions",
    generate_content_config=json_response_config,
)

# Define inspiration_agent
inspiration_agent = Agent(
    model="gemini-2.0-flash",
    name="inspiration_agent",
    description="A travel inspiration agent who inspire users, and discover their next vacations; Provide information about places, activities, interests.",
    instruction=prompt.INSPIRATION_AGENT_INSTR,
    tools=[
        AgentTool(agent=weather_agent), # <-- FIX IS HERE! Wrap weather_agent with AgentTool
        AgentTool(agent=place_agent),
        AgentTool(agent=poi_agent),
        map_tool # Assuming map_tool is already a FunctionTool or similar BaseTool instance
    ],
)