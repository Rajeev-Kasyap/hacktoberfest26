import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv("backend/.env")
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

try:
    completion = client.chat.completions.create(
        model="llama-3.2-90b-vision-preview",
        messages=[{"role": "user", "content": "Hello"}]
    )
    print("SUCCESS: ", completion.choices[0].message.content)
except Exception as e:
    print("FAILED: ", e)
