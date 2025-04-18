import json
import openai

# Step 1: Configure the API client
openai.api_key = "sk-96e2096fd7d54063844bdfbdd022c1ff"
openai.base_url = "https://api.deepseek.com"  # Replace with the actual endpoint if needed

# Step 2: Define Tools
def calculator_tool(operation: str, num1: float, num2: float):
    """
    Perform basic arithmetic operations like addition, subtraction, multiplication, or division.
    """
    if operation == "add":
        return num1 + num2
    elif operation == "subtract":
        return num1 - num2
    elif operation == "multiply":
        return num1 * num2
    elif operation == "divide":
        if num2 == 0:
            raise ValueError("Cannot divide by zero.")
        return num1 / num2
    else:
        raise ValueError(f"Unsupported operation: {operation}")

def search_tool(query: str):
    """
    Perform a web search for the given query (mock implementation).
    """
    return f"Search results for '{query}': [Mock results from the web]"

# Step 3: Describe Tools for the Model
tools = [
    {
        "type": "function",
        "function": {
            "name": "calculator_tool",
            "description": "Perform basic arithmetic operations like addition, subtraction, multiplication, or division.",
            "parameters": {
                "type": "object",
                "properties": {
                    "operation": {"type": "string", "enum": ["add", "subtract", "multiply", "divide"]},
                    "num1": {"type": "number"},
                    "num2": {"type": "number"}
                },
                "required": ["operation", "num1", "num2"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "search_tool",
            "description": "Perform a web search for the given query.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string"}
                },
                "required": ["query"]
            }
        }
    }
]

# Step 4: Map Tool Names to Implementations
tool_map = {
    "calculator_tool": calculator_tool,
    "search_tool": search_tool
}

# Step 5: Create the Agent
def agent_with_tools(prompt):
    try:
        # Use the new OpenAI client (introduced in v1.0.0)
        client = openai.OpenAI(api_key=openai.api_key, base_url=openai.base_url)
        
        # Send the request to the model with tool descriptions
        response = client.chat.completions.create(
            model="deepseek-chat",  # Replace with the correct model name
            messages=[{"role": "user", "content": prompt}],
            tools=tools,                  # Provide the tool descriptions
            tool_choice="auto"            # Let the model decide which tool to use
        )
        
        # Extract the response
        response_message = response.choices[0].message
        
        # Check if the model wants to use a tool
        if response_message.tool_calls:
            tool_call = response_message.tool_calls[0]
            tool_name = tool_call.function.name
            tool_args = json.loads(tool_call.function.arguments)
            
            # Execute the selected tool
            if tool_name in tool_map:
                tool_function = tool_map[tool_name]
                tool_result = tool_function(**tool_args)
                return f"Tool Result: {tool_result}"
            else:
                return f"Unknown tool: {tool_name}"
        else:
            return f"Model Response: {response_message.content.strip()}"
    
    except Exception as e:
        return f"An error occurred: {e}"

# Step 6: Interact with the Agent
if __name__ == "__main__":
    # Example usage
    user_input = "What is 5 multiplied by 3?"
    print(agent_with_tools(user_input))
    
    user_input = "Search for the latest AI research."
    print(agent_with_tools(user_input))