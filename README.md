# Solo-Leveling Health App

This repository contains a scaffold for a cross‑platform mobile app (iOS and Android) that integrates with popular health tracking services. The goal is to motivate users to become stronger through daily guidance and a ranking system.

## Features

- **Checklist**: Daily list of dos and don'ts for training and diet.
- **Third-Party Integrations**:
  - Apple Health / Apple Watch via HealthKit.
  - Garmin devices via the Garmin Health API.
  - MyFitnessPal for nutrition logging.
- **Workout & Meal Logging**: Add workouts and meals directly in the app while syncing data from connected services so everything stays in one place.
- **Food Database**: Bundled list of foods with macronutrients and micronutrients sourced from OpenFoodFacts for easy meal entry.
- **Calorie Estimator**: Calculate daily energy expenditure from height, weight, age, gender and activity level with optional body fat percentage for fat‑free mass adjustments.
- **Ranking**: Points are earned from program difficulty and how consistently goals are met. Extra credit goes to the most difficult programs that maintain a 95% completion rate. Rankings (E through S+) compare each user's points to the rest of the community once per day.

## Project Structure

```
client/        – React Native application
server/        – Express.js backend (original)
python_server/ – Flask backend implementing the same API
```

This repository currently only provides a minimal scaffold. Future commits should add authentication, data models, and additional API routes.

## Getting Started

1. Install Node dependencies:
   ```bash
   npm install
   ```
2. Install Python dependencies for the Flask server:
   ```bash
   pip install -r python_server/requirements.txt
   ```
3. Install client dependencies and start the Expo development server:
   ```bash
   cd client
   npm install
   npm start
   ```
4. Run the Flask API server:
   ```bash
   python python_server/app.py
   ```
5. Edit the files inside `client/` to build out the UI and integrate with device APIs. Use `addWorkout` and `addMeal` helpers in the client to post new entries to the server.
6. POST your height, weight, age, gender, and activity level to `/api/calories` on the Flask server to calculate daily energy expenditure.

See `docs/ARCHITECTURE.md` for more technical notes.
