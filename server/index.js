const express = require('express');
const fs = require('fs');
const path = require('path');
const app = express();
app.use(express.json());
const PORT = process.env.PORT || 3000;

app.get('/', (req, res) => {
  res.json({ message: 'Solo-Leveling server is running.' });
});

// Simple in-memory users list for demo purposes
const users = [
  { id: 1, difficulty: 7, consistency: 0.9 },
  { id: 2, difficulty: 4, consistency: 0.8 },
  { id: 3, difficulty: 9, consistency: 0.95 },
  { id: 4, difficulty: 5, consistency: 0.6 },
  { id: 5, difficulty: 6, consistency: 0.85 },
  { id: 6, difficulty: 8, consistency: 0.7 },
  { id: 7, difficulty: 10, consistency: 0.92 },
  { id: 8, difficulty: 3, consistency: 0.5 },
  { id: 9, difficulty: 4, consistency: 0.95 },
  { id: 10, difficulty: 9, consistency: 0.88 },
  { id: 11, difficulty: 6, consistency: 0.77 },
];

// Simple in-memory workout and meal logs
const workouts = [];
const meals = [];

// Load food dataset
let foods = [];
try {
  const dataPath = path.join(__dirname, '../data/foods.json');
  foods = JSON.parse(fs.readFileSync(dataPath, 'utf8'));
} catch (err) {
  console.warn('Could not load foods dataset', err.message);
}

function computePoints(user, list) {
  // Base points heavily weight consistency to discourage gaming the system
  let points = user.difficulty * Math.pow(user.consistency, 2);

  // Determine bonus for high difficulty programs that are regularly followed
  if (user.consistency >= 0.95) {
    const highCompliance = list
      .filter((u) => u.consistency >= 0.95)
      .sort((a, b) => b.difficulty - a.difficulty);
    const index = highCompliance.findIndex((u) => u.id === user.id);
    if (index !== -1) {
      // Highest difficulty gets the largest bonus
      const bonus = highCompliance.length - index;
      points += bonus;
    }
  }

  return points;
}

function getRank(user, list) {
  const sorted = [...list].sort((a, b) => computePoints(b, list) - computePoints(a, list));
  const index = sorted.findIndex((u) => u.id === user.id);

  if (index < 10) return 'S+';
  const percentile = (index / list.length) * 100;
  if (percentile < 5) return 'S';
  if (percentile < 10) return 'A';
  if (percentile < 20) return 'B';
  if (percentile < 30) return 'C';
  if (percentile < 40) return 'D';
  return 'E';
}

// Endpoint to fetch a user's rank based on their points
app.get('/api/rank', (req, res) => {
  const id = parseInt(req.query.id, 10) || 1;
  const user = users.find((u) => u.id === id);
  if (!user) {
    return res.status(404).json({ error: 'User not found' });
  }
  const rank = getRank(user, users);
  res.json({ rank });
});

// Add a workout entry
app.post('/api/workouts', (req, res) => {
  const entry = {
    id: workouts.length + 1,
    ...req.body,
  };
  workouts.push(entry);
  res.status(201).json(entry);
});

// Add a meal entry
app.post('/api/meals', (req, res) => {
  const entry = {
    id: meals.length + 1,
    ...req.body,
  };
  meals.push(entry);
  res.status(201).json(entry);
});

// Get list of foods with macro/micronutrients
app.get('/api/foods', (req, res) => {
  res.json(foods);
});

app.listen(PORT, () => {
  console.log(`Server listening on port ${PORT}`);
});
