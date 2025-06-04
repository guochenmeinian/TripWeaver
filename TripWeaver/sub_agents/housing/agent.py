from google.adk.agents import Agent
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StdioServerParameters
from TripWeaver.sub_agents.housing import prompt

# third party airbnb mcp: https://github.com/openbnb-org/mcp-server-airbnb?tab=readme-ov-file
airbnb_tool = MCPToolset(
    connection_params=StdioServerParameters(
        command="npx",
        args=["-y", "@openbnb/mcp-server-airbnb", "--ignore-robots-txt"]
    )
)

housing_agent = Agent(
    name="housing_agent",
    model="gemini-2.0-flash",
    description="Generates housing options based on user input.",
    instruction=prompt.HOUSING_AGENT_INSTR,
    tools=[
        airbnb_tool
    ],
)
