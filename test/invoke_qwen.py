

# from langchain.chat_models import ChatOpenAI
# from langchain_community.chat_models import ChatOpenAI
from langchain_openai import ChatOpenAI

from langchain.schema import HumanMessage

# Replace YOUR_API_KEY with your actual API key.
api_key = "sk-5a3fe1f20d1a408e8560ded9f2e22525"

# Configure ChatOpenAI to use Qwen2.5
chat = ChatOpenAI(
    model="qwen-plus",                # The model name should match what's expected on the server
    openai_api_key=api_key,         # Use your Qwen2.5 API key here
    openai_api_base="https://dashscope.aliyuncs.com/compatible-mode/v1"   # Replace with the actual endpoint URL
)

# Example usage: Sending a message to the model
messages = [HumanMessage(content="Hello, how are you?")]
response = chat(messages)

print(response.content)