# agent.py
"""Demonstration of Travel AI Coceirge using Agent Development Kit"""

from google.adk.agents import Agent
from google.adk.agents import LlmAgent
from TripWeaver.prompt import ROOT_AGENT_INSTR
from TripWeaver.sub_agents.inspiration.agent import inspiration_agent
from TripWeaver.sub_agents.pre_trip.agent import pre_trip_agent
# from TripWeaver.sub_agents.planning.agent import planning_agent
from TripWeaver.sub_agents.housing.agent import airbnb_agent
from TripWeaver.tools.memory import _load_precreated_itinerary

sub_agents = [
    inspiration_agent,
    pre_trip_agent,
    airbnb_agent, 
]


root_agent = LlmAgent(
    model="gemini-2.0-flash-001",
    name="root_agent",
    description="A Travel Conceirge using the services of multiple sub-agents",
    instruction=ROOT_AGENT_INSTR,
    sub_agents=sub_agents,
    before_agent_callback=_load_precreated_itinerary,
)