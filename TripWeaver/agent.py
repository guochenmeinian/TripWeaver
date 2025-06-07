# agent.py
"""Demonstration of Travel AI Coceirge using Agent Development Kit"""

from google.adk.agents import Agent
from google.adk.agents import LlmAgent
from TripWeaver.prompt import ROOT_AGENT_INSTR
from TripWeaver.sub_agents.inspiration.agent import inspiration_agent
from TripWeaver.sub_agents.pre_trip.agent import pre_trip_agent
# from TripWeaver.sub_agents.planning.agent import planning_agent
from TripWeaver.sub_agents.housing.agent import housing_agent
from TripWeaver.tools.memory import _load_precreated_itinerary

SequentialAgentGroup(
    agents=[
        pre_trip_agent,       # 收集 trip_plan + 偏好信息
        # weather_agent,        # 根据 trip_plan 查询城市天气
        inspiration_agent, 
        housing_agent,
        # planning_agent,       # 根据 trip_plan 和 候选项 生成行程
    ]
)


root_agent = LlmAgent(
    model="gemini-2.0-flash-001",
    name="root_agent",
    description="A Travel Conceirge using the services of multiple sub-agents",
    instruction=ROOT_AGENT_INSTR,
    sub_agents=sub_agents,
    before_agent_callback=_load_precreated_itinerary,
)