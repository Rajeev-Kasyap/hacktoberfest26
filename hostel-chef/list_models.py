import urllib.request, json, os
from dotenv import load_dotenv
load_dotenv("backend/.env")
key = os.getenv("GEMINI_API_KEY")
url = f"https://generativelanguage.googleapis.com/v1beta/models?key={key}"
req = urllib.request.Request(url)
try:
    with urllib.request.urlopen(req) as resp:
        models = json.loads(resp.read())["models"]
        for m in models:
            if "gemma" in m["name"].lower():
                print(m["name"])
except Exception as e:
    print(e)
