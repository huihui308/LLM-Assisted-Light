import os
from openai import OpenAI


# Set your API key as an environment variable
os.environ["DASHSCOPE_API_KEY"] = "sk-5a3fe1f20d1a408e8560ded9f2e22525"



"""
client = OpenAI(
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx",
    api_key=os.getenv("DASHSCOPE_API_KEY"),  # 如何获取API Key：https://help.aliyun.com/zh/model-studio/developer-reference/get-api-key
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)

completion = client.chat.completions.create(
    model="deepseek-r1",  # 此处以 deepseek-r1 为例，可按需更换模型名称。
    messages=[
        {'role': 'user', 'content': '9.9和9.11谁大'}
    ]
)

# 通过reasoning_content字段打印思考过程
print("思考过程：")
print(completion.choices[0].message.reasoning_content)

# 通过content字段打印最终答案
print("最终答案：")
print(completion.choices[0].message.content)
"""



"""
import os
from openai import OpenAI

client = OpenAI(
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx",
    api_key=os.getenv("DASHSCOPE_API_KEY"), 
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)
completion = client.chat.completions.create(
    model="qwen-plus", # 此处以qwen-plus为例，可按需更换模型名称。模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
    messages=[
        {'role': 'system', 'content': 'You are a helpful assistant.'},
        {'role': 'user', 'content': '你是谁？'}],
    )
    
print(completion.model_dump_json())
"""




import os
from dashscope import Generation

# Set your API key as an environment variable
os.environ["DASHSCOPE_API_KEY"] = "sk-5a3fe1f20d1a408e8560ded9f2e22525"

# Function to call Qwen model
def call_qwen(prompt):
    response = Generation.call(
        model="qwen-plus",  # Specify the model version
        # model="deepseek-r1",
        prompt=prompt,
        api_key=os.getenv("DASHSCOPE_API_KEY"),
        max_tokens=100  # Adjust based on your needs
    )
    
    return response.output.text if response.status_code == 200 else f"Error: {response.message}"


# Define the QwenAgent class
class QwenAgent:
    def __init__(self):
        self.tools = {}  # Dictionary to store available tools

    def add_tool(self, tool_name, tool_function):
        """Add a tool to the agent."""
        self.tools[tool_name] = tool_function

    def execute_tool(self, tool_name, *args, **kwargs):
        """Execute a specific tool by name."""
        if tool_name in self.tools:
            return self.tools[tool_name](*args, **kwargs)
        else:
            return f"Tool '{tool_name}' not found."

    def respond_to_query(self, query):
        """Generate a response using Qwen."""
        response = call_qwen(query)
        return response

# Example usage
if __name__ == "__main__":
    agent = QwenAgent()

    # Define some basic tools (you can replace these with actual functions)
    def weather_tool(city):
        return f"The weather in {city} is sunny today."

    def calculator_tool(expression):
        try:
            result = eval(expression)
            return f"The result of {expression} is {result}."
        except Exception as e:
            return f"Error evaluating expression: {e}"

    # Add tools to the agent
    agent.add_tool("weather", weather_tool)
    agent.add_tool("calculator", calculator_tool)

    # Interact with the agent
    print("Welcome to the Qwen Agent! Type 'exit' to quit.")
    while True:
        user_input = input("User: ")
        
        if user_input.lower() == "exit":
            print("Goodbye!")
            break
        
        # Check if user wants to use a tool
        if user_input.startswith("tool:"):
            parts = user_input.split(" ", 1)
            tool_name = parts[0].split(":")[1]
            tool_args = parts[1] if len(parts) > 1 else ""
            
            # Execute the tool with arguments
            tool_response = agent.execute_tool(tool_name, tool_args)
            print(f"Agent: {tool_response}")
        else:
            # Use Qwen to respond to general queries
            response = agent.respond_to_query(user_input)
            print(f"Agent: {response}")