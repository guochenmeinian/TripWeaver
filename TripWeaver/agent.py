# agent.py
"""Demonstration of Travel AI Coceirge using Agent Development Kit"""

from google.adk.agents import Agent
from TripWeaver.prompt import ROOT_AGENT_INSTR
from TripWeaver.sub_agents.inspiration.agent import inspiration_agent
# from TripWeaver.sub_agents.pre_trip.agent import pre_trip_agent
# from TripWeaver.sub_agents.planning.agent import planning_agent
from TripWeaver.tools.memory import _load_precreated_itinerary

root_agent = Agent(
    model="gemini-2.0-flash-001",
    name="root_agent",
    description="A Travel Conceirge using the services of multiple sub-agents",
    instruction=ROOT_AGENT_INSTR,
    sub_agents=[
        inspiration_agent,
    #     planning_agent,
    #     pre_trip_agent,
    #     in_trip_agent,
    #     post_trip_agent,
    ],
    before_agent_callback=_load_precreated_itinerary,
)