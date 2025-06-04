from google.adk.agents import Agent
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StdioServerParameters
from TripWeaver.sub_agents.housing import prompt

airbnb_agent = Agent(
    name="airbnb_agent",
    model="gemini-2.0-flash",
    description="Generates housing options based on user input.",
    instruction=prompt.AIRBNB_AGENT_INSTR,
    tools=[
        # third party airbnb mcp: https://github.com/openbnb-org/mcp-server-airbnb?tab=readme-ov-file
        MCPToolset(
            connection_params=StdioServerParameters(
                command="npx",
                args=["-y", "@openbnb/mcp-server-airbnb", "--ignore-robots-txt"]
            )
        )
    ],
)
