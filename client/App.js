import React from 'react';
import { StyleSheet, Text, View } from 'react-native';
import { addWorkout, addMeal } from './api';

export default function App() {
  return (
    <View style={styles.container}>
      <Text>Welcome to the Solo-Leveling Health App!</Text>
      <Text>Use addWorkout and addMeal helpers to submit your data.</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
    alignItems: 'center',
    justifyContent: 'center',
  },
});
