import re
with open("backend/main.py", "r") as f:
    content = f.read()

old_parser = """    with urllib.request.urlopen(req, timeout=120) as resp:
        result = json.loads(resp.read().decode("utf-8"))
        return result["candidates"][0]["content"]["parts"][0]["text"].strip()"""

new_parser = """    with urllib.request.urlopen(req, timeout=120) as resp:
        result = json.loads(resp.read().decode("utf-8"))
        parts = result["candidates"][0]["content"]["parts"]
        # Thinking models return thoughts as the first part(s). We want the final actual text response.
        final_text = ""
        for p in reversed(parts):
            if "thought" not in p or not p["thought"]:
                final_text = p["text"]
                break
        return final_text.strip()"""

content = content.replace(old_parser, new_parser)
with open("backend/main.py", "w") as f:
    f.write(content)
print("Gemini parser patched!")
