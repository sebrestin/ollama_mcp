import asyncio
import inspect
from typing import Any, Callable, List

import sys
import json
import os

from mcp.client.sse import sse_client
from mcp.client.session import ClientSession

class MCPClient:
    def __init__(self, server_url: str):
        self.server_url = server_url

    async def list_tools(self):
        """Fetches the list of tools from the MCP server."""
        # Note: We create a new session just to list tools.
        # Ideally we'd keep a persistent session, but for this simple client 
        # establishing a connection when needed is robust.
        async with sse_client(self.server_url) as streams:
            async with ClientSession(streams[0], streams[1]) as session:
                await session.initialize()
                result = await session.list_tools()
                return result.tools

    async def call_tool(self, name: str, arguments: dict) -> Any:
        """Calls a tool on the MCP server."""
        async with sse_client(self.server_url) as streams:
            async with ClientSession(streams[0], streams[1]) as session:
                await session.initialize()
                result = await session.call_tool(name, arguments)
                # Return the text content of the result
                output = []
                if result.content:
                    for content in result.content:
                        if hasattr(content, 'text'):
                            output.append(content.text)
                        else:
                            output.append(str(content))
                return "\n".join(output)

class ToolWrapper:

    PARAM_TYPE_MAP = {
        "string": str,
        "number": float,
        "integer": int,
        "boolean": bool,
        "array": list,
        "object": dict,
    }

    def __init__(self, client: MCPClient, tool_info: Any):
        self.client = client
        self.name = tool_info.name
        self.description = tool_info.description
        
        self.__name__ = self.name
        self.__doc__ = self.description
        
        # Construct the signature based on inputSchema
        schema = tool_info.inputSchema
        parameters = []
        
        required_params = set(schema.get("required", []))
        properties = schema.get("properties", {})
        
        annotations = {}
        
        for param_name, param_schema in properties.items():
            param_type = param_schema.get("type", "string")
            
            # Map JSON types to Python types
            annotations[param_name] = self.PARAM_TYPE_MAP.get(param_type, Any)
            
            # Determine if default value is needed
            default = inspect.Parameter.empty
            if param_name not in required_params:
                default = None # Or construct from schema if 'default' is present
                
            parameters.append(
                inspect.Parameter(
                    name=param_name,
                    kind=inspect.Parameter.KEYWORD_ONLY,
                    default=default,
                    annotation=annotations[param_name]
                )
            )
            
        self.__annotations__ = annotations
        
        # Assign a proper signature object for introspection
        sig = inspect.Signature(parameters=parameters)
        self.__signature__ = sig

    def __call__(self, **kwargs) -> Any:
        # We use asyncio.run to call the async server method from this sync wrapper
        return asyncio.run(self.client.call_tool(self.name, kwargs))


class ToolBox:
    def __init__(self, mcp_servers_config: dict = None):
        self.clients = []
        if mcp_servers_config:
            for name, server_config in mcp_servers_config.items():
                url = server_config.get("url")
                if url:
                    self.clients.append(MCPClient(url))

    def load_tools(self) -> List[Callable]:
        """
        Connects to the MCP servers, fetches available tools, and returns
        a list of callable python functions that proxy to the servers.
        """
        all_wrappers = []
        for client in self.clients:
            try:
                tools_info = asyncio.run(client.list_tools())
                for tool in tools_info:
                    all_wrappers.append(ToolWrapper(client, tool))
            except Exception as e:
                print(f"Error loading tools from client {client.server_url}: {e}", file=sys.stderr)
        
        return all_wrappers
# Backward compatibility / Convenience
# Calling load_tools() at import time might fail if server is down,
# but passing functions is required.
# We will not execute it at top level to avoid import side effects,
# but agent/main.py will need to call load_tools().
