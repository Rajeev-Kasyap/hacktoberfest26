import urllib.request, json, os
from dotenv import load_dotenv
load_dotenv("backend/.env")
key = os.getenv("GEMINI_API_KEY")

prompt = """You are a highly skilled but incredibly sarcastic chef. 

Write a genuinely delicious, high-quality recipe using SOME OR ALL of these ingredients: banana, milk, oil, chilli powder, muesli
CRITICAL RULES:
1. You DO NOT have to use every ingredient! Only use the ones that make culinary sense together. If you see clashing ingredients (like milk and oil), aggressively throw away the bad ones.
2. Kitchen tools you are ALLOWED to use (use only the ones the dish actually needs, ignore the rest): microwave. You may also assume salt and water.
3. The recipe steps must be a straightforward, normal cookbook recipe (3-5 short steps).
4. Do not make it a 'survival' or 'sad' meal. Make it sound like a legitimate, elevated dish.
5. Keep all the heavy sarcasm confined to the title and the description.
6. Do not mention any ingredient that you decided to throw away.

Reply ONLY with raw JSON in this exact format:
{
  "recipe_title": "string",
  "description": "string",
  "steps": ["string", "string"]
}"""

url = f"https://generativelanguage.googleapis.com/v1beta/models/gemma-4-31b-it:generateContent?key={key}"
payload = {
    "contents": [{"parts": [{"text": prompt}]}],
    "generationConfig": {"temperature": 0.8}
}
req = urllib.request.Request(url, data=json.dumps(payload).encode(), headers={"Content-Type": "application/json"})
try:
    with urllib.request.urlopen(req) as resp:
        print(resp.read().decode())
except Exception as e:
    print(e)
    if hasattr(e, 'read'):
        print(e.read().decode())
