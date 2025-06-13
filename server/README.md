# Server

This directory contains the original Express.js backend used to experiment with the ranking logic. It remains for reference but a Python/Flask implementation is available under `python_server/`.

This server stores user data and calculates a daily rank for each user. Points are determined by program difficulty and squared consistency. Programs that keep a 95% completion rate receive an additional difficulty bonus. The server also accepts workout and meal entries so data from Garmin or MyFitnessPal can be consolidated. Ranks are assigned by comparing each user's points to everyone else.

## Development

Install dependencies from the repository root:
```bash
npm install express
```

Run the server:
```bash
node server/index.js
```

### Endpoints
- `GET /api/rank?id=<userId>` – return the user's rank
- `POST /api/workouts` – add a workout entry to the log
- `POST /api/meals` – add a meal entry to the log
- `GET /api/foods` – list foods with macro and micronutrients
