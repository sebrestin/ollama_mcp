import pandas as pd
import openmeteo_requests
import requests_cache
from retry_requests import retry

from mcp.server.fastmcp import FastMCP

import tools as tools


# Initialize FastMCP server``
mcp = FastMCP("ollama-tools-server", host="0.0.0.0", port=8000)


mcp.add_tool(tools.get_weather)
mcp.add_tool(tools.current_date)


if __name__ == "__main__":
    # Run the MCP server with SSE transport
    mcp.run(transport='sse')

