import ollama


from toolbox import ToolBox
import agent

import json
import os


with open("mcp_server_config.json", "r") as f:
    config = json.load(f)

toolbox = ToolBox(config.get("mcpServers", {}))
available_tools = toolbox.load_tools()

a = agent.Agent(model="qwen3", thinking=True, tools=available_tools)
a.start()
