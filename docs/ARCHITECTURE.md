# Architecture Overview

This project includes both a Node/Express backend and an equivalent Python/Flask backend. The frontend is a React Native app built with Expo.

## Client

- Implemented in **React Native**.
- Retrieves health metrics from device APIs or third-party services.
- Displays a daily checklist of tasks for the user.
- Communicates with the server for authentication, logging workouts/meals, ranking updates, and calorie calculations.

### Health Integrations

- **Apple HealthKit**: Use a library like `react-native-health` to request step counts, workouts, and other metrics on iOS.
- **Garmin Health API**: Garmin requires registration to access device data. The client polls the server, which in turn communicates with Garmin's REST API.
  Workout information from Garmin devices is consolidated with manually added logs.
- **MyFitnessPal**: There is no official public API. Users may export data manually or connect through an intermediate service.
    Once retrieved, nutrition data is stored alongside workouts so users only enter it once.
- **Food Database**: A local JSON file (`data/foods.json`) containing foods with macro and micronutrients is loaded by both servers and served through `/api/foods`.

## Server

- Built with **Express.js** (TypeScript) or **Flask** (Python).
- Stores user profiles, goals, daily checklist completion, workout logs, meal logs, and ranking data in a database.
- Provides endpoints for the mobile client to retrieve tasks, submit progress, add workouts and meals, and calculate calorie needs.

## Calorie Estimation

The `/api/calories` endpoint calculates a user's daily energy expenditure. When a body fat percentage is supplied, the server uses the Katch‑McArdle formula based on lean mass; otherwise it defaults to the Mifflin‑St Jeor equation. The result is multiplied by an activity multiplier to return total daily energy expenditure (TDEE).

## Ranking Logic

Each user earns **points** based on the difficulty of their program and how consistently they complete it. Consistency is squared in the formula to discourage setting an unrealistic difficulty and ignoring it. Programs with a 95% or better completion rate receive a bonus ordered by difficulty so the hardest regularly followed program scores the highest. The server compares each user's points to everyone else's to assign ranks.

| Rank | Percentile |
|------|------------|
| S+   | Top 10 users |
| S    | Top 5% |
| A    | Top 10% |
| B    | Top 20% |
| C    | Top 30% |
| D    | Top 40% |
| E    | Rest |

Ranks are recalculated daily after metrics are synced.

Future iterations might add notifications, more elaborate weighting formulas, and social features.
