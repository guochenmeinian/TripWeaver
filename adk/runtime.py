# adk/runtime.py
class ADKRuntime:
    def __init__(self):
        self.agents = {}
        self.connections = {}

    def register(self, name: str, agent):
        self.agents[name] = agent

    def connect(self, from_agent: str, to_agent: str):
        self.connections[from_agent] = to_agent

    def run(self, start_agent: str, input_data: dict) -> dict:
        current_agent = start_agent
        data = input_data
        while current_agent:
            agent = self.agents[current_agent]
            data = agent.run(data)
            current_agent = self.connections.get(current_agent)
        return data
