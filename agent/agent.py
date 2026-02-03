import ollama

class Agent:

    STOP_MARK = "stop"

    def __init__(self, model: str, thinking: bool, tools: list):
        self._model = model
        self._thinking = thinking
        self._tools = {tool.__name__: tool for tool in tools}
        self._context = list()
    
    def start(self):
        while True:
            message = input("What's on your mind? \n")
            if message == self.STOP_MARK:
                break
            self.process_request(message)

    def process_request(self, message):
        self._context.append({"role": "user", "content": message})

        while True:

            response = ollama.chat(
                model=self._model,
                messages=self._context,
                tools=self._tools.values(),
                stream=True,
                think=self._thinking
            )

            thinking = ""
            content = ""
            tool_calls = list()

            done_thinking = False
            
            for chunk in response:
                if chunk.message.thinking:
                    thinking += chunk.message.thinking
                    print(chunk.message.thinking, end="", flush=True)
                if chunk.message.content:
                    if not done_thinking:
                        done_thinking = True
                        print("\n")
                    content += chunk.message.content
                    print(chunk.message.content, end="", flush=True)
                if chunk.message.tool_calls:
                    tool_calls.extend(chunk.message.tool_calls)
                    print(chunk.message.tool_calls)

            if thinking or content or tool_calls:
                self._context.append(
                    {
                        "role": "assistant",
                        "thinking": thinking,
                        "content": content,
                        "tool_calls": tool_calls
                    }
                )
            
            if not tool_calls:
                break

            for tool_call in tool_calls:

                tool_name = tool_call.function.name
                tool_args = tool_call.function.arguments
                tool_func = self._tools[tool_name]
                tool_result = tool_func(**tool_args)

                self._context.append({"role": "tool", "tool_name": tool_name, "content": tool_result})

                response = ollama.chat(
                    model=self._model,
                    messages=self._context,
                    tools=self._tools.values(),
                    stream=True,
                    think=self._thinking
                )
               
        print("\n")

        return response