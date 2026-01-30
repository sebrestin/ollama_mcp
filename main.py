import ollama

import agent
import tools


available_tools = [tools.get_weather, tools.current_date]

a = agent.Agent(model="qwen3", thinking=True, tools=available_tools)
a.start()
