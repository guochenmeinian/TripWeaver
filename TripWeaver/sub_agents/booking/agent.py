# booking/agent.py

from google.adk.agents import Agent
from TripWeaver.sub_agents.booking import prompt

booking_agent = Agent(
    name="booking_agent",
    model="gemini-2.0-flash",
    description="Helps book flights, select seats, and reserve hotels for the user.",
    instruction=prompt.BOOKING_AGENT_INSTR,
)
