import os
import requests
from dotenv import load_dotenv

load_dotenv("backend/.env")
hf_token = os.environ.get("HF_TOKEN")

API_URL = "https://api-inference.huggingface.co/models/google/gemma-2-2b-it"
headers = {"Authorization": f"Bearer {hf_token}"}

response = requests.post(API_URL, headers=headers, json={"inputs": "Write a recipe for cereal."})
print(response.json())
