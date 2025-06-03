# sub_agents/housing/airbnb_agent.py
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StdioServerParameters
from google.adk.agents import Agent
from TripWeaver.sub_agents.housing import prompt

airbnb_agent = Agent(
    name="airbnb_agent",
    model="gemini-2.0-flash",
    description="Generates housing options based on user input.",
    instruction=prompt.AIRBNB_AGENT_INSTR,
    tools=[
        MCPToolset(
            connection_params=StdioServerParameters(
                command="npx",
                args=["-y", "@openbnb/mcp-server-airbnb"]
            )
        )
    ],
)