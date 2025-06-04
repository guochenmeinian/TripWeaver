# TripWeaver/sub_agents/pre_trip/collector_agent.py
from google.adk.agents import Agent
from TripWeaver.sub_agents.pre_trip.prompt import UPDATE_PROFILE_INSTR, PRETRIP_COLLECTOR_INSTR
from TripWeaver.shared_libraries.types import GeminiUserProfile, json_response_config
from google.adk.tools.agent_tool import AgentTool

update_profile_agent = Agent(
    name="update_profile_agent",
    model="gemini-2.0-flash",
    description="Conversationally gathers missing user profile fields",
    instruction=UPDATE_PROFILE_INSTR,
    disallow_transfer_to_parent=True,
    disallow_transfer_to_peers=True,
    output_schema=GeminiUserProfile,
    output_key="user_profile",
    generate_content_config=json_response_config
)

pre_trip_agent = Agent(
    name="pre_trip_agent",
    model="gemini-2.0-flash",
    description="Conversationally gathers missing user profile fields",
    instruction=PRETRIP_COLLECTOR_INSTR,
    tools=[AgentTool(agent=update_profile_agent)],
)


