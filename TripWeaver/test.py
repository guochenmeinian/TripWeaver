import google.adk
print(dir(google.adk))
# 看看输出中是否有 'agent_groups'
from google.adk import agent_groups
print(dir(agent_groups))
# 看看输出中是否有 'ParallelAgentGroup' 或 'SequentialAgentGroup'