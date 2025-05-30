# adk/agent.py
class Agent:
    def run(self, input_data: dict, **kwargs) -> dict:
        raise NotImplementedError("Each agent must implement the run method.")
