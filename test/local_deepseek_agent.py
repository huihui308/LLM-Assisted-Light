from langchain.llms.base import LLM
from typing import Optional, List, Mapping, Any
import requests
from langchain.agents import initialize_agent, Tool
from langchain.agents import AgentType

# Custom LLM Wrapper for Ollama
class OllamaLLM(LLM):
    model_name: str = "deepseek"
    base_url: str = "http://localhost:11434/api/generate"

    def _call(self, prompt: str, stop: Optional[List[str]] = None) -> str:
        headers = {"Content-Type": "application/json"}
        data = {
            "model": self.model_name,
            "prompt": prompt,
            "stream": False
        }

        response = requests.post(self.base_url, headers=headers, json=data)

        if response.status_code == 200:
            result = response.json()
            return result.get("response", "")
        else:
            raise Exception(f"Ollama API error: {response.status_code}, {response.text}")
    
    @property
    def _identifying_params(self) -> Mapping[str, Any]:
        return {"name_of_model": self.model_name}

    @property
    def _llm_type(self) -> str:
        return "custom"

# Define Tools
def search(query: str) -> str:
    return f"Search result for '{query}'"

tools = [
    Tool(
        name="Search",
        func=search,
        description="Useful for searching the web."
    )
]

# Initialize Ollama LLM and Agent
ollama_llm = OllamaLLM(model_name="deepseek-r1:8b")
agent = initialize_agent(tools, ollama_llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)

# Run the Agent
response = agent.run("What is the tallest mountain?")
print(response)