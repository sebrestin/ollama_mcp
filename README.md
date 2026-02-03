# Ollama AI Agent with Model Context Protocol (MCP)

A Python-based conversational AI agent that leverages [Ollama](https://ollama.com/) for local LLM inference and the **Model Context Protocol (MCP)** for extensible tool usage. The agent acts as an MCP Client, connecting to an MCP Server to execute tools like weather fetching and date retrieval.

## 🌟 Features

- **Model Context Protocol (MCP)**: Uses a standardized protocol to connect the Agent (Client) with Tools (Server).
- **Interactive Chat Interface**: Conversational agent with streaming responses.
- **Thinking Mode**: Optional reasoning display showing the model's thought process.
- **Weather Data**: Fetch historical weather data using the Open-Meteo API.
- **Docker Support**: Full containerized setup Orchestrating Agent, Tools Server, and Ollama.
- **Dev Container**: VS Code dev container configuration for easy development.

## 🏗️ Project Structure

The project is split into an Agent Client and a Tools Server:

```
ollama_mcp/
├── agent/                  # MCP Client ( The AI Agent )
│   ├── agent.py            # Core Agent class
│   ├── main.py             # Entry point for the Agent
│   └── toolbox.py          # MCP Tool handling
├── tools/                  # MCP Server ( The Tools )
│   ├── main.py             # Entry point for the MCP Server
│   └── tools.py            # Tool definitions (weather, date)
├── mcp_server_config.json  # Configuration for connecting Agent to Tools
├── dockers/
│   ├── Dockerfile          # Shared container image
│   └── docker-compose.yml  # Orchestration
└── requirements.txt        # Dependencies
```

## 🚀 Getting Started

### Prerequisites

- Docker and Docker Compose
- NVIDIA GPU with Docker GPU support (recommended)
- Python 3.12+ (if running locally)

### Option 1: Docker (Recommended)

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd ollama_mcp
   ```

2. **Start the services**:
   This will start the Ollama container, the Tools Server, and the Agent.
   ```bash
   docker-compose -f dockers/docker-compose.yml up -d
   ```

3. **Pull the required model**:
   ```bash
   docker exec -it ollama_mcp-ollama-1 ollama pull qwen3
   ```
   *(Note: Container name might vary, check with `docker ps`)*

4. **Run the Agent**:
   Since the agent runs interactively, you might want to run it directly:
   ```bash
   # If building a separate agent container, or running locally, see below.
   # The default compose setup runs services.
   ```
   *Correction*: The `docker-compose.yml` likely sets up the environment. If you want to chat, you usually run the agent script.
   
   If you want to run the agent interactively inside the container:
   ```bash
   docker-compose -f dockers/docker-compose.yml run --rm tools python /workspaces/ollama_mcp/agent/main.py
   ```
   *(Assuming the environment allows connecting to the running tools service)*

### Option 2: Local Development

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Start the Tools Server**:
   Open a terminal and run:
   ```bash
   python tools/main.py
   ```
   This starts the MCP Server on port 8000.

3. **Configure the Agent**:
   Edit `mcp_server_config.json` to point to your local server instead of the docker hostname:
   ```json
   {
     "mcpServers": {
       "default": {
         "url": "http://localhost:8000/sse"
       }
     }
   }
   ```

4. **Start the Agent**:
   In a separate terminal:
   ```bash
   python agent/main.py
   ```

## 🛠️ Available Tools

Tools are provided by the MCP Server in `tools/`:

### `get_weather(lat, lon, start_date, end_date)`
Fetches historical weather data from the Open-Meteo Archive API.

### `current_date()`
Returns the current date.

## 🔧 Customization

### Adding New Tools
1. Define the function in `tools/tools.py`.
2. Register it in `tools/main.py`:
   ```python
   mcp.add_tool(tools.my_new_tool)
   ```
3. Restart the Tools Server. The Agent will automatically discover the new tool on next startup.

## 📦 Dependencies

- `mcp`: The Model Context Protocol SDK.
- `ollama`: Python client for Ollama.
- `pandas`, `openmeteo-requests`: For the weather tool.
