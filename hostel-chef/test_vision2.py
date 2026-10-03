import urllib.request, json, os, base64
from dotenv import load_dotenv
load_dotenv("backend/.env")
key = os.getenv("GEMINI_API_KEY")
url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={key}"
b64 = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNk+A8AAQUBAScY42YAAAAASUVORK5CYII="
payload = {"contents": [{"parts": [{"text": "What is in this image?"}, {"inlineData": {"mimeType": "image/png", "data": b64}}]}]}
req = urllib.request.Request(url, data=json.dumps(payload).encode(), headers={"Content-Type": "application/json"})
try:
    with urllib.request.urlopen(req) as resp:
        print("Vision OK:", resp.read().decode()[:100])
except Exception as e:
    print("Error:", e, e.read().decode() if hasattr(e, 'read') else "")
