with open("backend/main.py", "r") as f:
    content = f.read()
    
# I will just write it fresh from the correct version
new_main = """from fastapi import FastAPI, UploadFile, Form, File
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
from functools import lru_cache
import base64
import json
import re
import urllib.request

from dotenv import load_dotenv

load_dotenv()

OLLAMA_URL = "http://127.0.0.1:11434/api/generate"
OLLAMA_MODEL = "gemma4:e2b"

app = FastAPI(title="2 AM Hostel Chef API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def ollama(prompt: str, schema: Optional[dict] = None, temperature: float = 0.0,
           images: Optional[List[str]] = None, timeout: int = 300) -> str:
    payload = {
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False,
        "think": False,
        "options": {"temperature": temperature},
    }
    if schema:
        payload["format"] = schema
    if images:
        payload["images"] = images
    req = urllib.request.Request(
        OLLAMA_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8"))["response"].strip()


def extract_json(raw: str) -> dict:
    raw = raw.strip()
    fenced = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", raw, re.DOTALL)
    if fenced:
        return json.loads(fenced.group(1))
    start = raw.find("{")
    end = raw.rfind("}")
    return json.loads(raw[start:end + 1])


def decide_ingredients(items: List[str]):
    tags = {}
    batch_prompt = \"\"\"Classify the following food items for cooking.
For each item, assign:
role: main (primary food), seasoning (spice/flavoring), cooking_fat (oil, butter), liquid (milk, water), or staple (salt, sugar).
taste: sweet, savory, or both.

Items: \"\"\" + ", ".join(items) + \"\"\"

Reply ONLY with raw JSON in this exact format:
{
  "banana": {"role": "main", "taste": "sweet"},
  "oil": {"role": "cooking_fat", "taste": "both"}
}\"\"\"

    try:
        raw_tags = ollama(batch_prompt, temperature=0.1)
        parsed = extract_json(raw_tags)
        for x in items:
            key = x.lower()
            if key in parsed:
                tags[x] = (parsed[key].get("role", "main"), parsed[key].get("taste", "both"))
            else:
                tags[x] = ("main", "both")
    except Exception as e:
        print("Batch tag error:", e)
        tags = {x: ("main", "both") for x in items}

    votes = {"sweet": 0.0, "savory": 0.0}
    for role, taste in tags.values():
        if taste in votes:
            if role == "main":
                votes[taste] += 1.0
            elif role == "seasoning":
                votes[taste] += 0.5

    if votes["sweet"] == votes["savory"]:
        profile = "both"
    else:
        profile = max(votes, key=votes.get)

    keep, drop = [], []
    for x, (role, taste) in tags.items():
        clashes = profile != "both" and taste not in (profile, "both")
        fat_in_sweet = profile == "sweet" and role == "cooking_fat"
        (drop if (clashes or fat_in_sweet) else keep).append(x)

    if not keep:
        keep, drop = list(items), []
    return profile, keep, drop, tags


RECIPE_SCHEMA = {
    "type": "object",
    "properties": {
        "recipe_title": {"type": "string"},
        "description": {"type": "string"},
        "steps": {"type": "array", "items": {"type": "string"}},
    },
    "required": ["recipe_title", "description", "steps"],
}


def build_recipe_prompt(keep: List[str], equip_list: list, profile: str) -> str:
    equip = ", ".join(equip_list) if equip_list else "bare hands"
    return f\"\"\"You are a highly skilled but incredibly sarcastic chef. 

Write a genuinely delicious, high-quality recipe using these ingredients: {", ".join(keep)}
You DO NOT have to use every ingredient! Only use the ones that make culinary sense for a normal, tasty dish. You may assume salt and water.
Kitchen tools you are ALLOWED to use (use only the ones the dish actually needs, ignore the rest): {equip}

Rules:
- The recipe steps must be a straightforward, normal cookbook recipe (3-5 short steps).
- Do not make it a 'survival' or 'sad' meal. Make it sound like a legitimate dish.
- Keep all the heavy sarcasm confined to the title and the description.
- Do not mention any ingredient that is not in the list above.\"\"\"


@app.get("/")
def read_root():
    return {"message": "Hostel Chef AI Backend is alive."}


def parse_items(text: str) -> List[str]:
    parts = re.split(r"[,\n;]| and ", text)
    items = []
    for p in parts:
        p = re.sub(r"^[\s\-\*\d\.\)]+", "", p).strip(" .")
        if p and p.lower() not in [i.lower() for i in items]:
            items.append(p)
    return items[:12]


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
        encoded = [base64.b64encode(await img.read()).decode("utf-8") for img in images]
        try:
            photo_ingredients = ollama(
                "List ONLY the food items that are CLEARLY and OBVIOUSLY visible in these photos. "
                "Do not guess or invent items. Output a simple comma separated list, nothing else.",
                images=encoded, timeout=180,
            )
            print("VISION:", photo_ingredients)
        except Exception as e:
            print("Ollama Vision error:", e)

    items = parse_items(", ".join(x for x in [ingreds, photo_ingredients] if x))
    if not items:
        items = ["random scraps found on the floor"]

    try:
        profile, keep, drop, tags = decide_ingredients(items)
        print(f"PIPELINE profile={profile} keep={keep} drop={drop}")

        raw = ollama(build_recipe_prompt(keep, equip_list, profile), RECIPE_SCHEMA, temperature=0.8)
        data = json.loads(raw)
        data["steps"] = [
            f"{i}. {re.sub(r'^\s*\d+[\.\)]\s*', '', s).strip()}"
            for i, s in enumerate(data["steps"], 1)
        ]
        data["model_used"] = f"Powered by Local {OLLAMA_MODEL}"
        return data
    except Exception as e:
        print("Ollama error:", e)
        return {
            "recipe_title": "Local AI Offline Situation",
            "description": "Something crashed locally, but you still gotta eat.",
            "steps": ["1. Stare at your food.", "2. Microwave it."],
            "model_used": "offline mock",
        }
"""
with open("backend/main.py", "w") as f:
    f.write(new_main)
print("File rewritten clean!")
