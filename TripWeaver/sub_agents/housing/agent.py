from google.adk.agents import Agent
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StdioServerParameters
from TripWeaver.sub_agents.housing import prompt

airbnb_tool = MCPToolset(
    connection_params=StdioServerParameters(
        command="npx",
        args=["-y", "@openbnb/mcp-server-airbnb", "--ignore-robots-txt"]
    )
)

def make_housing_agent():
    return Agent(
        name="housing_agent",
        model="gemini-2.0-flash-001", 
        description="Generates housing options based on user input.",
        instruction=prompt.HOUSING_AGENT_INSTR,
        tools=[airbnb_tool],
    )
