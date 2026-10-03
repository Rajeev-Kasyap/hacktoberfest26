import re
with open("backend/main.py", "r") as f:
    content = f.read()

old_logic = """    photo_ingredients = ""
    if images:
        encoded_images = []
        for img in images:
            data = await img.read()
            encoded_images.append({
                "mime_type": img.content_type or "image/jpeg",
                "data": base64.b64encode(data).decode("utf-8")
            })
        try:
            photo_ingredients = call_gemini(
                VISION_MODEL,
                "List ONLY the food items that are CLEARLY and OBVIOUSLY visible in these photos. Do not guess. Output a simple comma separated list, nothing else.",
                encoded_images
            )
            print("VISION:", photo_ingredients)
        except Exception as e:
            print("Vision error:", e)

    parts = re.split(r"[,\n;]| and ", ", ".join(x for x in [ingreds, photo_ingredients] if x))"""

new_logic = """    parts = re.split(r"[,\n;]| and ", ingreds)"""

content = content.replace(old_logic, new_logic)

with open("backend/main.py", "w") as f:
    f.write(content)
print("Vision stripped from backend!")
