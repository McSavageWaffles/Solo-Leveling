from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)

# In-memory user data
users = [
    {"id": 1, "difficulty": 7, "consistency": 0.9},
    {"id": 2, "difficulty": 4, "consistency": 0.8},
    {"id": 3, "difficulty": 9, "consistency": 0.95},
    {"id": 4, "difficulty": 5, "consistency": 0.6},
    {"id": 5, "difficulty": 6, "consistency": 0.85},
    {"id": 6, "difficulty": 8, "consistency": 0.7},
    {"id": 7, "difficulty": 10, "consistency": 0.92},
    {"id": 8, "difficulty": 3, "consistency": 0.5},
    {"id": 9, "difficulty": 4, "consistency": 0.95},
    {"id": 10, "difficulty": 9, "consistency": 0.88},
    {"id": 11, "difficulty": 6, "consistency": 0.77},
]

workouts = []
meals = []

# Load food dataset
foods = []
try:
    data_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'foods.json')
    with open(data_path) as f:
        foods = json.load(f)
except Exception as e:
    print(f"Could not load foods dataset: {e}")


def compute_points(user, user_list):
    points = user["difficulty"] * (user["consistency"] ** 2)
    if user["consistency"] >= 0.95:
        high = sorted(
            [u for u in user_list if u["consistency"] >= 0.95],
            key=lambda u: u["difficulty"],
            reverse=True,
        )
        try:
            index = [u["id"] for u in high].index(user["id"])
            bonus = len(high) - index
            points += bonus
        except ValueError:
            pass
    return points


def get_rank(user, user_list):
    sorted_users = sorted(user_list, key=lambda u: compute_points(u, user_list), reverse=True)
    try:
        index = [u["id"] for u in sorted_users].index(user["id"])
    except ValueError:
        return "E"

    if index < 10:
        return "S+"
    percentile = (index / len(sorted_users)) * 100
    if percentile < 5:
        return "S"
    if percentile < 10:
        return "A"
    if percentile < 20:
        return "B"
    if percentile < 30:
        return "C"
    if percentile < 40:
        return "D"
    return "E"


@app.route("/", methods=["GET"])
def root():
    return jsonify({"message": "Solo-Leveling Python server running"})


@app.route("/api/rank", methods=["GET"])
def rank():
    user_id = int(request.args.get("id", 1))
    user = next((u for u in users if u["id"] == user_id), None)
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify({"rank": get_rank(user, users)})


@app.route("/api/workouts", methods=["POST"])
def add_workout():
    entry = {"id": len(workouts) + 1}
    entry.update(request.json or {})
    workouts.append(entry)
    return jsonify(entry), 201


@app.route("/api/meals", methods=["POST"])
def add_meal():
    entry = {"id": len(meals) + 1}
    entry.update(request.json or {})
    meals.append(entry)
    return jsonify(entry), 201


@app.route("/api/foods", methods=["GET"])
def list_foods():
    return jsonify(foods)


# Estimate daily calorie expenditure based on physical metrics.
# Expects JSON: {
#   "gender": "male"|"female",
#   "age": int,
#   "height_cm": float,
#   "weight_kg": float,
#   "activity": float,  # multiplier like 1.2 for sedentary
#   "body_fat": float (optional percentage)
# }
# Returns BMR and TDEE. If body_fat is provided, uses Katch-McArdle,
# otherwise defaults to Mifflin-St Jeor formula.
@app.route("/api/calories", methods=["POST"])
def estimate_calories():
    data = request.json or {}
    gender = data.get("gender", "male").lower()
    age = float(data.get("age", 0))
    height = float(data.get("height_cm", 0))
    weight = float(data.get("weight_kg", 0))
    activity = float(data.get("activity", 1.2))
    body_fat = data.get("body_fat")

    if body_fat is not None:
        # Katch-McArdle BMR using lean mass
        lean_mass = weight * (1 - float(body_fat) / 100)
        bmr = 370 + 21.6 * lean_mass
    else:
        bmr = 10 * weight + 6.25 * height - 5 * age
        if gender == "male":
            bmr += 5
        else:
            bmr -= 161

    tdee = bmr * activity
    return jsonify({"bmr": round(bmr, 2), "tdee": round(tdee, 2)})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
