# Ollama AI Agent with Tool Calling

A Python-based conversational AI agent that leverages [Ollama](https://ollama.com/) for local LLM inference with tool-calling capabilities. The agent can interact with external tools to fetch real-time data like weather information and current dates.

## 🌟 Features

- **Interactive Chat Interface**: Conversational agent with streaming responses
- **Tool Calling**: Extensible tool system that allows the LLM to call Python functions
- **Thinking Mode**: Optional reasoning display showing the model's thought process
- **Weather Data**: Fetch historical weather data using the Open-Meteo API
- **Docker Support**: Containerized setup with GPU support for Ollama
- **Dev Container**: VS Code dev container configuration for easy development

## 🏗️ Project Structure

```
ollama_mcp/
├── agent.py              # Core Agent class with chat loop and tool execution
├── tools.py              # Tool definitions (weather, date)
├── main.py               # Entry point to start the agent
├── requirements.txt      # Python dependencies
├── dockers/
│   ├── Dockerfile        # Container image with Ollama and Python
│   └── docker-compose.yml # Docker Compose configuration with GPU support
└── .devcontainer/
    └── devcontainer.json # VS Code dev container settings
```

## 🚀 Getting Started

### Prerequisites

- Docker and Docker Compose
- NVIDIA GPU with Docker GPU support (optional, but recommended)
- Python 3.12+ (if running locally)

### Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd ollama_mcp
   ```

2. **Install dependencies** (if running locally):
   ```bash
   pip install -r requirements.txt
   ```

3. **Start Ollama service** (using Docker):
   ```bash
   docker-compose -f dockers/docker-compose.yml up -d
   ```

4. **Pull the required model**:
   ```bash
   docker exec -it <container-name> ollama pull qwen3
   ```

### Running the Agent

**Local execution**:
```bash
python main.py
```

**Using VS Code Dev Container**:
1. Open the project in VS Code
2. Click "Reopen in Container" when prompted
3. Run `python main.py` in the integrated terminal

## 💬 Usage

Once the agent starts, you'll see the prompt:
```
What's on your mind?
```

You can ask questions that require tool usage:
- "What's the weather in Cluj-Napoca for yesterday?"
- "What's today's date?"
- "Get me the weather data for coordinates 46.77, 23.59 from 2026-01-28 to 2026-01-28"

To exit the agent, type:
```
stop
```

## 🛠️ Available Tools

### `get_weather(lat, lon, start_date, end_date)`
Fetches historical weather data from the Open-Meteo Archive API.

**Parameters**:
- `lat` (float): Latitude of the location
- `lon` (float): Longitude of the location
- `start_date` (str): Start date in YYYY-MM-DD format
- `end_date` (str): End date in YYYY-MM-DD format

**Returns**: JSON string containing daily weather metrics including temperature, precipitation, wind, sunshine duration, and more.

### `current_date()`
Returns the current date in YYYY-MM-DD format.

## 🔧 Customization

### Adding New Tools

1. Define your tool function in `tools.py`:
   ```python
   def my_custom_tool(param1: str, param2: int) -> str:
       """Description of what the tool does.
       
       :param param1: Description of param1
       :param param2: Description of param2
       :return: Description of return value
       """
       # Your implementation
       return result
   ```

2. Register the tool in `main.py`:
   ```python
   available_tools = [tools.get_weather, tools.current_date, tools.my_custom_tool]
   ```

### Changing the Model

Edit `main.py` to use a different Ollama model:
```python
a = agent.Agent(model="llama3.2", thinking=True, tools=available_tools)
```

### Disabling Thinking Mode

Set `thinking=False` when initializing the agent:
```python
a = agent.Agent(model="qwen3", thinking=False, tools=available_tools)
```

## 🐳 Docker Configuration

The project includes Docker support with GPU acceleration:

- **Ollama Service**: Runs on port `11434`
- **GPU Support**: Configured for NVIDIA GPUs with all capabilities
- **Persistent Storage**: Weather data cache and Ollama models are persisted in Docker volumes

## 📦 Dependencies

Key dependencies include:
- `ollama`: Python client for Ollama
- `pandas`: Data manipulation for weather data
- `openmeteo-requests`: Open-Meteo API client
- `requests-cache`: HTTP caching for API requests
- `retry-requests`: Automatic retry logic for failed requests

See `requirements.txt` for the complete list.

## 🧠 How It Works

1. **User Input**: The agent receives a message from the user
2. **LLM Processing**: Ollama processes the message with access to tool definitions
3. **Tool Calling**: If needed, the LLM generates tool calls with appropriate parameters
4. **Tool Execution**: The agent executes the requested tools and collects results
5. **Response Generation**: The LLM uses tool results to formulate a final response
6. **Streaming Output**: Responses are streamed in real-time, including thinking process (if enabled)

## 📝 License

This project is provided as-is for educational and development purposes.

## 🤝 Contributing

Feel free to submit issues, fork the repository, and create pull requests for any improvements.

## 🔗 Resources

- [Ollama Documentation](https://github.com/ollama/ollama)
- [Open-Meteo API](https://open-meteo.com/)
- [Ollama Python Library](https://github.com/ollama/ollama-python)
