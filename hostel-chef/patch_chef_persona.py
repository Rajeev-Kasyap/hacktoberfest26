import re
with open("backend/main.py", "r") as f:
    content = f.read()

old_prompt_func = re.search(r"def build_recipe_prompt.*?\"\"\"", content, re.DOTALL).group(0)

new_prompt_func = """def build_recipe_prompt(keep: List[str], equip_list: list, profile: str) -> str:
    equip = ", ".join(equip_list) if equip_list else "bare hands"
    return f\"\"\"You are a highly skilled but incredibly sarcastic chef. 

Write a genuinely delicious, high-quality recipe using these ingredients: {", ".join(keep)}
You DO NOT have to use every ingredient! Only use the ones that make culinary sense for a normal, tasty dish. You may assume salt and water.
Kitchen tools you are ALLOWED to use (use only the ones the dish actually needs, ignore the rest): {equip}

Rules:
- The recipe steps must be a straightforward, normal cookbook recipe (3-5 short steps).
- Do not make it a 'survival' or 'sad' meal. Make it sound like a legitimate dish.
- Keep all the heavy sarcasm confined to the title and the description.
- Do not mention any ingredient that is not in the list above.\"\"\""""

content = content.replace(old_prompt_func, new_prompt_func)

with open("backend/main.py", "w") as f:
    f.write(content)
print("Persona patched!")
