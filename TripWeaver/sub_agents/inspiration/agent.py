
"""Inspiration agent. A pre-booking agent covering the ideation part of the trip."""

from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool
from TripWeaver.shared_libraries.types import GeminiSpotSuggestions, POISuggestions, json_response_config
from TripWeaver.sub_agents.inspiration import prompt
from TripWeaver.tools.places import map_tool
from TripWeaver.tools.weather import weather_tool

weather_agent = Agent(
    model="gemini-2.0-flash",
    name="weather_agent",
    description="This agent provides weather information given a place",
    instruction=prompt.WEATHER_AGENT_INSTR,
    disallow_transfer_to_parent=True,
    disallow_transfer_to_peers=True,
)

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

inspiration_agent = Agent(
    model="gemini-2.0-flash",
    name="inspiration_agent",
    description="A travel inspiration agent who inspire users, and discover their next vacations; Provide information about places, activities, interests.",
    instruction=prompt.INSPIRATION_AGENT_INSTR,
    tools=[weather_agent, AgentTool(agent=place_agent), AgentTool(agent=poi_agent), map_tool],
)
