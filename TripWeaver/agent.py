# agent.py
"""Demonstration of Travel AI Concierge using Agent Development Kit"""

from google.adk.agents import LlmAgent
from google.adk.agent_groups import SequentialAgentGroup
from TripWeaver.prompt import ROOT_AGENT_INSTR

# Sub-agents
from TripWeaver.sub_agents.pre_trip.agent import pre_trip_agent        # 收集 trip_plan + 偏好信息
from TripWeaver.sub_agents.inspiration.agent import inspiration_agent  # 根据 trip_plan 和 weather 给出灵感
from TripWeaver.sub_agents.housing.agent import housing_agent          # 查找住宿
# from TripWeaver.sub_agents.activities.agent import activities_agent  # 可选：更具体的活动推荐
# from TripWeaver.sub_agents.planning.agent import planning_agent      # 可选：最终 itinerary 编排

# State pre-load
from TripWeaver.tools.memory import _load_precreated_itinerary


# Define parallel group for housing + activities
parallel_housing_activities = ParallelAgentGroup(
    name="parallel_housing_activities",
    agents=[
        housing_agent,
        activities_agent
    ]
)

# Define full pipeline
sub_agents = SequentialAgentGroup(
    name="trip_pipeline",
    agents=[
        pre_trip_agent,              # Step 1: 收集 trip_plan + 偏好
        inspiration_agent,           # Step 2: 获取天气和兴趣方向
        parallel_housing_activities, # Step 3: 并行获取住宿 + 活动建议
        # planning_agent             # Step 4: 构建最终 daily_itinerary_plan
    ]
)

# Define root agent
root_agent = Agent(
    model="gemini-2.0-flash-001",
    name="root_agent",
    description="A Travel Concierge using the services of multiple sub-agents",
    instruction=ROOT_AGENT_INSTR,
    sub_agents=sub_agents,
    before_agent_callback=_load_precreated_itinerary,
)
