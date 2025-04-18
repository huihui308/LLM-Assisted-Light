
"""
from langchain.llms.base import LLM
from langchain.agents import initialize_agent, Tool
from typing import Any, List, Mapping, Optional
import requests

# Step 1: Create a Custom DeepSeek Wrapper
class DeepSeek(LLM):
    api_key: str
    model_name: str = "deepseek-resoner"
    api_url: str = "https://api.deepseek.com"  # Replace with actual endpoint

    def _call(self, prompt: str, stop: Optional[List[str]] = None) -> str:
        headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}
        data = {"model": self.model_name, "prompt": prompt, "max_tokens": 100, "stop": stop or []}
        response = requests.post(self.api_url, headers=headers, json=data)
        response.raise_for_status()
        return response.json()["choices"][0]["text"]

    @property
    def _identifying_params(self) -> Mapping[str, Any]:
        return {"model_name": self.model_name}

    @property
    def _llm_type(self) -> str:
        return "deepseek"

# Step 2: Define Tools for the Agent
def search_web(query):
    return f"Search results for: {query}"

def calculate(expression):
    try:
        result = eval(expression)
        return f"The result of {expression} is {result}"
    except Exception as e:
        return f"Error calculating expression: {e}"

tools = [
    Tool(name="Search", func=search_web, description="Useful for searching the web."),
    Tool(name="Calculator", func=calculate, description="Useful for performing calculations.")
]

# Step 3: Initialize the Agent
api_key = "sk-96e2096fd7d54063844bdfbdd022c1ff"  # Replace with your actual API key
llm = DeepSeek(api_key=api_key)
agent = initialize_agent(tools=tools, llm=llm, agent="zero-shot-react-description", verbose=True)

# Step 4: Run the Agent
query = "What is the capital of France, and what is 10 * 5?"
response = agent.run(query)
print(response)
"""



# https://python.langchain.com/api_reference/deepseek/chat_models/langchain_deepseek.chat_models.ChatDeepSeek.html

# Instantiate:
from langchain_deepseek import ChatDeepSeek

llm = ChatDeepSeek(
    model="deepseek-chat",
    # model="deepseek-reasoner",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
    api_key="sk-96e2096fd7d54063844bdfbdd022c1ff",
    # other params...
)


# Invoke:
messages = [
    ("system", "You are a helpful translator. Translate the user sentence to French."),
    ("human", "I love programming."),
]
llm.invoke(messages)


# Stream:
for chunk in llm.stream(messages):
    print(chunk.text(), end="")

stream = llm.stream(messages)
full = next(stream)
for chunk in stream:
    full += chunk
full


# Async:
import asyncio
# await llm.ainvoke(messages)

# stream:
# async for chunk in (await llm.astream(messages))

# batch:
# await llm.abatch([messages])


# Tool calling:
from pydantic import BaseModel, Field

class GetWeather(BaseModel):
    '''Get the current weather in a given location'''

    location: str = Field(..., description="The city and state, e.g. San Francisco, CA")

class GetPopulation(BaseModel):
    '''Get the current population in a given location'''

    location: str = Field(..., description="The city and state, e.g. San Francisco, CA")

llm_with_tools = llm.bind_tools([GetWeather, GetPopulation])
ai_msg = llm_with_tools.invoke("Which city is hotter today and which is bigger: LA or NY?")
ai_msg.tool_calls
print(ai_msg.tool_calls)


# Structured output:
from typing import Optional

from pydantic import BaseModel, Field

class Joke(BaseModel):
    '''Joke to tell user.'''

    setup: str = Field(description="The setup of the joke")
    punchline: str = Field(description="The punchline to the joke")
    rating: Optional[int] = Field(description="How funny the joke is, from 1 to 10")

structured_llm = llm.with_structured_output(Joke)
structured_llm.invoke("Tell me a joke about cats")


# Token usage:
ai_msg = llm.invoke(messages)
ai_msg.usage_metadata


# Response metadata
ai_msg = llm.invoke(messages)
ai_msg.response_metadata
