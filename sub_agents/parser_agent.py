# agents/parser_agent.py
from adk.agent import Agent

class PreferenceParserAgent(Agent):
    def run(self, input_data: dict, **kwargs) -> dict:
        user_input = input_data.get("query", "")
        # 简化的解析逻辑
        return {
            "departure": "New York",
            "start_date": "2025-06-10",
            "end_date": "2025-06-18",
            "transport": "self-drive",
            "preferences": ["nature", "culture"]
        }
