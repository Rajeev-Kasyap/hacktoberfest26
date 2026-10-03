import re
with open("backend/main.py", "r") as f:
    content = f.read()

# Replace the single tagger with a batch tagger
old_tag_section = """TAG_SCHEMA = {
    "type": "object",
    "properties": {
        "role": {"type": "string", "enum": ["main", "seasoning", "cooking_fat", "liquid", "staple"]},
        "taste": {"type": "string", "enum": ["sweet", "savory", "both"]},
    },
    "required": ["role", "taste"],
}


@lru_cache(maxsize=512)
def tag_ingredient(name: str) -> tuple:
    prompt = f\"\"\"Classify the food item "{name}" for cooking.
role: main (a primary food, e.g. banana, paneer, bread, maggi), seasoning (spice/sauce/flavoring, e.g. chilli powder, masala, ketchup), cooking_fat (oil, butter, ghee), liquid (milk, water, juice, curd), staple (salt, sugar).
taste: sweet (normally eaten in sweet dishes), savory (normally eaten in savory dishes), both (used in either).
Answer for the single item only.\"\"\"
    try:
        t = json.loads(ollama(prompt, TAG_SCHEMA))
        return (t["role"], t["taste"])
    except Exception as e:
        print("tag error:", name, e)
        return ("main", "both")  # unknown -> neutral, never silently dropped


def decide_ingredients(items: List[str]):
    \"\"\"Pick the dominant taste profile and drop whatever clashes with it.\"\"\"
    tags = {x: tag_ingredient(x.lower()) for x in items}"""

new_tag_section = """def decide_ingredients(items: List[str]):
    \"\"\"Pick the dominant taste profile and drop whatever clashes with it.\"\"\"
    tags = {}
    
    # Batch tag all ingredients in one call to save massive time
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
        tags = {x: ("main", "both") for x in items}"""

content = content.replace(old_tag_section, new_tag_section)

with open("backend/main.py", "w") as f:
    f.write(content)
print("Batch tag patched!")
