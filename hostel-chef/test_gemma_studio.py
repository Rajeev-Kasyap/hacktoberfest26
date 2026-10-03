import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv("backend/.env")
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

try:
    model = genai.GenerativeModel('gemma-2-9b-it')
    response = model.generate_content("Say hello in 3 words.")
    print("SUCCESS:", response.text)
except Exception as e:
    print("FAILED:", e)
