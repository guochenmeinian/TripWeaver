# # agent.py
# """Demonstration of Travel AI Concierge using Agent Development Kit"""

# from google.adk.agents import LlmAgent
# from google.adk.agents import SequentialAgent # Import SequentialAgent directly from google.adk.agents
# from google.adk.agents import ParallelAgent   # Import ParallelAgent directly from google.adk.agents

# from TripWeaver.prompt import ROOT_AGENT_INSTR

# # Sub-agents
# from TripWeaver.sub_agents.pre_trip.agent import pre_trip_agent        # 收集 trip_plan + 偏好信息
# from TripWeaver.sub_agents.inspiration.agent import inspiration_agent  # 根据 trip_plan 和 weather 给出灵感
# from TripWeaver.sub_agents.housing.agent import housing_agent          # 查找住宿
# # from TripWeaver.sub_agents.activities.agent import activities_agent  # Optional: more specific activity recommendations
# from TripWeaver.sub_agents.planning.agent import planning_agent      # Optional: final itinerary orchestration

# # State pre-load
# from TripWeaver.tools.memory import _load_precreated_itinerary


# # Define parallel group for housing + activities
# parallel_housing_activities = ParallelAgent(
#     name="parallel_housing_activities",
#     sub_agents=[
#         housing_agent
#         # activities_agent # Uncomment when activities_agent is defined and imported
#     ]
# )

# # Define full pipeline
# sub_agents_group = SequentialAgent( # Renamed variable to avoid confusion, though 'sub_agents' is fine.
#     name="trip_pipeline",
#     sub_agents=[
#         # pre_trip_agent,              # Step 1: Collect trip plan + preferences
#         # inspiration_agent,           # Step 2: Get weather and inspiration
#         parallel_housing_activities, # Step 3: Parallel fetching of accommodation + activity suggestions
#         # planning_agent             # Step 4: Build final daily itinerary plan
#     ]
# )

# # Define root agent
# root_agent = LlmAgent(
#     model="gemini-2.0-flash-001",
#     name="root_agent",
#     description="A Travel Concierge using the services of multiple sub-agents",
#     instruction=ROOT_AGENT_INSTR,
#     # FIX: Ensure the single SequentialAgent instance is passed directly.
#     # The variable 'sub_agents_group' now holds the SequentialAgent instance.
#     sub_agents=sub_agents_group,
#     before_agent_callback=_load_precreated_itinerary,
# )

# agent.py
# """Demonstration of Travel AI Coceirge using Agent Development Kit"""

from google.adk.agents import Agent
from google.adk.agents import LlmAgent
from TripWeaver.prompt import ROOT_AGENT_INSTR
from TripWeaver.sub_agents.inspiration.agent import inspiration_agent
from TripWeaver.sub_agents.pre_trip.agent import pre_trip_agent
from TripWeaver.sub_agents.planning.agent import planning_agent
from TripWeaver.sub_agents.housing.agent import housing_agent
from TripWeaver.tools.memory import _load_precreated_itinerary

sub_agents = [
    pre_trip_agent,      
    inspiration_agent,
    planning_agent,
    housing_agent,
]


root_agent = LlmAgent(
    model="gemini-2.0-flash-001",
    name="root_agent",
    description="A Travel Conceirge using the services of multiple sub-agents",
    instruction=ROOT_AGENT_INSTR,
    sub_agents=sub_agents,
    before_agent_callback=_load_precreated_itinerary,
)