from google.adk.agents import Agent
from TripWeaver.sub_agents.planning import prompt

def get_weather(city: str) -> dict:
    """Retrieves the current weather report for a specified city.

    Args:
        city (str): The name of the city for which to retrieve the weather report.

    Returns:
        dict: status and result or error msg.
    """
    if city.lower() == "new york":
        return {
            "status": "success",
            "report": (
                "The weather in New York is sunny with a temperature of 25 degrees"
                " Celsius (77 degrees Fahrenheit)."
            ),
        }
    else:
        return {
            "status": "error",
            "error_message": f"Weather information for '{city}' is not available.",
        }

planning_agent = Agent(
    name="planning_agent",
    model="gemini-2.0-flash",
    description="Generates travel itineraries based on user input and optionally checks weather.",
    instruction=prompt.PLANNING_AGENT_INSTR,
    tools=[get_weather],  # 👈 你也可以继续添加更多工具
)
