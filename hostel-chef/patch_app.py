import re
with open("src/App.jsx", "r") as f:
    content = f.read()

# Remove imageFiles state
content = re.sub(r"const \[imageFiles,\s*setImageFiles\]\s*=\s*useState\(\[\]\);", "", content)

# Remove image upload handler
content = re.sub(r"const handleImageUpload\s*=\s*\(e\)\s*=>\s*\{.*?\};", "", content, flags=re.DOTALL)

# Remove images from formData
content = re.sub(r"imageFiles\.forEach\(f\s*=>\s*formData\.append\('images',\s*f\)\);", "", content)

# Remove the camera button UI (the whole label block)
content = re.sub(r"<label\s+htmlFor=\"image-upload\"[^>]*>.*?</label>", "", content, flags=re.DOTALL)

# Remove the image preview map block
content = re.sub(r"\{imageFiles\.length\s*>\s*0\s*&&\s*\(\s*<div[^>]*>.*?</div>\s*\)\s*\}", "", content, flags=re.DOTALL)

with open("src/App.jsx", "w") as f:
    f.write(content)
print("Vision stripped from frontend!")
