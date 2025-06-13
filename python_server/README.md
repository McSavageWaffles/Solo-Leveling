# Python Server

This directory contains a simple Flask backend that mirrors the functionality of the existing Express server. It stores user difficulty and consistency stats, allows logging of workouts and meals, and exposes a rank endpoint.

## Development

Install dependencies:
```bash
pip install -r requirements.txt
```

Run the server:
```bash
python app.py
```

### Endpoints
- `GET /api/rank?id=<userId>` – return the user's rank
- `POST /api/workouts` – add a workout entry
- `POST /api/meals` – add a meal entry
- `GET /api/foods` – list foods with macro and micronutrients
- `POST /api/calories` – estimate BMR and daily calories from height, weight, age, gender, activity and optional body fat percentage
