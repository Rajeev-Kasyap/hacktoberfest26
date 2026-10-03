from fastapi import FastAPI, UploadFile, Form, File
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
import base64
import json
import re
import urllib.request
import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
VISION_MODEL = "gemini-3.8-flash"
LOGIC_MODEL = "gemma-4-26b-a4b-it"

app = FastAPI(title="2 AM Hostel Chef API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def call_gemini(model: str, prompt: str, images_base64: List[dict] = None) -> str:
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={GEMINI_API_KEY}"
    
    parts = [{"text": prompt}]
    if images_base64:
        for img in images_base64:
            parts.append({
                "inlineData": {
                    "mimeType": img["mime_type"],
                    "data": img["data"]
                }
            })
            
    payload = {
        "contents": [{"parts": parts}],
        "generationConfig": {
            "temperature": 0.8
        }
    }
    
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=120) as resp:
        result = json.loads(resp.read().decode("utf-8"))
        parts = result["candidates"][0]["content"]["parts"]
        # Thinking models return thoughts as the first part(s). We want the final actual text response.
        final_text = ""
        for p in reversed(parts):
            if "thought" not in p or not p["thought"]:
                final_text = p["text"]
                break
        return final_text.strip()


def extract_json(raw: str) -> dict:
    raw = raw.strip()
    fenced = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", raw, re.DOTALL)
    if fenced:
        return json.loads(fenced.group(1))
    start = raw.find("{")
    end = raw.rfind("}")
    return json.loads(raw[start:end + 1])


def build_recipe_prompt(ingredients: str, equip_list: list) -> str:
    equip = ", ".join(equip_list) if equip_list else "bare hands"
    return f"""You are a highly skilled but incredibly sarcastic chef. 

Write a genuinely delicious, high-quality recipe using SOME OR ALL of these ingredients: {ingredients}
CRITICAL RULES:
1. You DO NOT have to use every ingredient! Only use the ones that make culinary sense together. If you see clashing ingredients (like milk and oil), aggressively throw away the bad ones.
2. Kitchen tools you are ALLOWED to use (use only the ones the dish actually needs, ignore the rest): {equip}. You may also assume salt and water.
3. The recipe steps must be a straightforward, normal cookbook recipe (3-5 short steps).
4. Do not make it a 'survival' or 'sad' meal. Make it sound like a legitimate, elevated dish.
5. Keep all the heavy sarcasm confined to the title and the description.
6. Do not mention any ingredient that you decided to throw away.

Reply ONLY with raw JSON in this exact format:
{{
  "recipe_title": "string",
  "description": "string",
  "steps": ["string", "string"]
}}"""


@app.get("/")
def read_root():
    return {"message": "Hostel Chef AI Backend is alive."}


@app.post("/api/cook")
async def generate_recipe(
    equipment: str = Form(...),
    ingredients_text: Optional[str] = Form(None),
    images: List[UploadFile] = File(None),
):
    equip_list = json.loads(equipment)
    ingreds = ingredients_text.strip() if ingredients_text else ""

    if not images and (not ingreds or ingreds.lower() in ["nothing", "air", "water", "none", "empty"] or len(ingreds) < 3):
        return {
            "recipe_title": "Sleep for Dinner",
            "description": "The ultimate hostel delicacy when you have literally nothing.",
            "steps": ["1. Drink tap water.", "2. Go to bed."],
            "model_used": "Powered by Sleep Deprivation",
        }

    photo_ingredients = ""
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

    parts = re.split(r"[,\n;]| and ", ", ".join(x for x in [ingreds, photo_ingredients] if x))
    items = []
    for p in parts:
        p = re.sub(r"^[\s\-\*\d\.\)]+", "", p).strip(" .")
        if p and p.lower() not in [i.lower() for i in items]:
            items.append(p)
    
    final_ingredients = ", ".join(items) if items else "random scraps found on the floor"

    try:
        raw = call_gemini(LOGIC_MODEL, build_recipe_prompt(final_ingredients, equip_list))
        data = extract_json(raw)
        data["steps"] = [
            f"{i}. {re.sub(r'^\s*\d+[\.\)]\s*', '', s).strip()}"
            for i, s in enumerate(data["steps"], 1)
        ]
        data["model_used"] = f"Powered by Cloud {LOGIC_MODEL}"
        return data
    except Exception as e:
        print("Logic error:", e)
        return {
            "recipe_title": "Cloud AI Offline Situation",
            "description": "The cloud crashed, but you still gotta eat.",
            "steps": ["1. Stare at your food.", "2. Microwave it."],
            "model_used": "offline mock",
        }
