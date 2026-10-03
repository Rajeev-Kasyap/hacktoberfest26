import urllib.request, json, os
from dotenv import load_dotenv
load_dotenv("backend/.env")
key = os.getenv("GEMINI_API_KEY")
url = f"https://generativelanguage.googleapis.com/v1beta/models/gemma-4-31b-it:generateContent?key={key}"
b64 = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNk+A8AAQUBAScY42YAAAAASUVORK5CYII="
payload = {"contents": [{"parts": [{"text": "What is in this image?"}, {"inlineData": {"mimeType": "image/png", "data": b64}}]}]}
req = urllib.request.Request(url, data=json.dumps(payload).encode(), headers={"Content-Type": "application/json"})
try:
    with urllib.request.urlopen(req) as resp:
        print("Vision supported!")
except Exception as e:
    print("Error:", e, e.read().decode() if hasattr(e, 'read') else "")
