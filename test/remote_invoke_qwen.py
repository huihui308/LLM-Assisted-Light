
import os
# from langchain.chat_models import ChatOpenAI
# from langchain_community.chat_models import ChatOpenAI
from langchain_openai import ChatOpenAI

from langchain.schema import HumanMessage

# Set your API key as an environment variable
os.environ["DASHSCOPE_API_KEY"] = "sk-5a3fe1f20d1a408e8560ded9f2e22525"


# Configure ChatOpenAI to use Qwen2.5
chat = ChatOpenAI(
    model="qwen-plus",                # The model name should match what's expected on the server
    openai_api_key=os.getenv("DASHSCOPE_API_KEY"),         # Use your Qwen2.5 API key here
    openai_api_base="https://dashscope.aliyuncs.com/compatible-mode/v1"   # Replace with the actual endpoint URL
)

# Example usage: Sending a message to the model
messages = [HumanMessage(content="Hello, how are you?")]
response = chat(messages)

print(response.content)