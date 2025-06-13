const API_URL = process.env.EXPO_PUBLIC_API_URL || 'http://localhost:3000';

export async function addWorkout(workout) {
  const res = await fetch(`${API_URL}/api/workouts`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(workout),
  });
  if (!res.ok) {
    throw new Error('Failed to add workout');
  }
  return res.json();
}

export async function addMeal(meal) {
  const res = await fetch(`${API_URL}/api/meals`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(meal),
  });
  if (!res.ok) {
    throw new Error('Failed to add meal');
  }
  return res.json();
}
