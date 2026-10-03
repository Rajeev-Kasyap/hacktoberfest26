import urllib.request, json
URL = "http://127.0.0.1:11434/api/generate"
# Valid 1x1 png base64
b64 = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNk+A8AAQUBAScY42YAAAAASUVORK5CYII="
payload = {
    "model": "gemma4:e2b",
    "prompt": "Test",
    "images": [b64, b64],
    "stream": False
}
req = urllib.request.Request(URL, data=json.dumps(payload).encode(), headers={"Content-Type": "application/json"})
try:
    urllib.request.urlopen(req)
    print("Multi image OK")
except Exception as e:
    print("Error on multi:", e)
