import json
import requests

API_URL = "https://world.openfoodfacts.org/cgi/search.pl"

# fetch 100 foods with macro and micro nutrients
params = {
    "search_simple": 1,
    "action": "process",
    "json": 1,
    "page_size": 100,
    "fields": "product_name,nutriments",
}

resp = requests.get(API_URL, params=params)
resp.raise_for_status()
data = resp.json()
foods = []
for p in data.get("products", []):
    name = p.get("product_name")
    nutriments = p.get("nutriments", {})
    if not name:
        continue
    food = {
        "name": name,
        "kcal": nutriments.get("energy-kcal_100g"),
        "protein": nutriments.get("proteins_100g"),
        "carbs": nutriments.get("carbohydrates_100g"),
        "fat": nutriments.get("fat_100g"),
        "fiber": nutriments.get("fiber_100g"),
        "salt": nutriments.get("salt_100g"),
    }
    foods.append(food)

with open("data/foods.json", "w") as f:
    json.dump(foods, f, indent=2)

print(f"Saved {len(foods)} foods to data/foods.json")
