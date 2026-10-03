import urllib.request, json
URL = "http://127.0.0.1:11434/api/generate"
payload = {
    "model": "gemma4:e2b",
    "prompt": "Test",
    "images": [],
    "stream": False
}
req = urllib.request.Request(URL, data=json.dumps(payload).encode(), headers={"Content-Type": "application/json"})
try:
    urllib.request.urlopen(req)
    print("Empty images array OK")
except Exception as e:
    print("Error on empty:", e)

# What if image is invalid base64?
payload["images"] = ["invalidbase64"]
req = urllib.request.Request(URL, data=json.dumps(payload).encode(), headers={"Content-Type": "application/json"})
try:
    urllib.request.urlopen(req)
    print("Invalid base64 OK")
except Exception as e:
    print("Error on invalid:", e)
