
import requests
import json

# Define the API endpoint
# OLLAMA_API_URL = "http://localhost:11434/api/generate"
OLLAMA_API_URL = "http://192.168.170.60:11434/api/generate"

# Specify the model name (e.g., deepseek-r1:7b or deepseek-r1:1.5b)
MODEL_NAME = "deepseek-r1:8b"  # Change this to the specific variant you want to use

# Define the input prompt
PROMPT = "Explain the concept of artificial intelligence."
# PROMPT = "What is your name."

# Prepare the request payload
payload = {
    "model": MODEL_NAME,
    "prompt": PROMPT,
    "stream": False  # Set to True if you want streaming responses
}

# Send the POST request to the Ollama API
response = requests.post(OLLAMA_API_URL, json=payload)

# Check if the request was successful
if response.status_code == 200:
    result = response.json()
    print("Response from Deepseek-R1:")
    print(result.get("response", "No response received"))
else:
    print(f"Error: {response.status_code}")
    print(response.text)