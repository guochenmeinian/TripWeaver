# TripWeaver/sub_agents/pre_trip/collector_agent.py
from google.adk.agents import Agent
from TripWeaver.sub_agents.pre_trip.prompt import UPDATE_PROFILE_INSTR, PRETRIP_COLLECTOR_INSTR, TRIP_PLAN_INSTR
from TripWeaver.shared_libraries.types import UserProfile, json_response_config, BasicTripPlanSchema
from google.adk.tools.agent_tool import AgentTool
from google.adk.agents import LlmAgent


update_profile_agent = Agent(
    name="update_profile_agent",
    model="gemini-2.0-flash",
    description="Conversationally gathers missing user profile fields",
    instruction=UPDATE_PROFILE_INSTR,
    disallow_transfer_to_parent=True,
    disallow_transfer_to_peers=True,
    output_schema=UserProfile,
    output_key="user_profile",
    generate_content_config=json_response_config
)

update_trip_plan_agent = Agent(
    name="update_trip_plan_agent",
    model="gemini-2.0-flash",
    description="Collects city-by-city travel plan from the user",
    instruction=TRIP_PLAN_INSTR,
    disallow_transfer_to_parent=True,
    disallow_transfer_to_peers=True,
    output_schema=BasicTripPlanSchema,
    output_key="trip_plan",
    generate_content_config=json_response_config,
)

pre_trip_agent = LlmAgent(
    name="pre_trip_agent",
    model="gemini-2.0-flash",
    description="Orchestrates user profile collection before trip generation",
    instruction=PRETRIP_COLLECTOR_INSTR,
    tools=[
        AgentTool(agent=update_profile_agent),
        AgentTool(agent=update_trip_plan_agent),
    ],
    
)

