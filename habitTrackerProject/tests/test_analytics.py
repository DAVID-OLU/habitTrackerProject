"""
This a Unit tests for the analytics module of the Habit Tracking application.

This module tests various functions in the analytics module, including streak calculations,
habit data formatting, and filtering of habits based on their streaks.
"""

import unittest
from analytics import get_longest_run_streak, get_habits_with_broken_streak, get_habits_with_longest_streak
from habit import Habit
from datetime import datetime
import json


class TestAnalytics(unittest.TestCase):
    """
    Test suite for verifying the functionality of analytics functions.
    """

    def test_get_longest_run_streak(self):
        """
        for testing the get_longest_run_streak function.

        Loads the habit from 'data/habits.json', and then converts each entry to a Habit object,
        and then asserts that the evaluated longest run streak is equal to the expected value.
        """
        with open('data/habits.json', 'r') as file:
            habits_data = json.load(file)
            habits = [Habit.from_dict(habit) for habit in habits_data]
            # The code assert that the longest streak computed matches the expected value
            self.assertEqual(get_longest_run_streak(habits), 10)

    def test_habit_tracked_data_date(self):
        """
        For testing the add_tracked_data method of the Habit class.

        Creates a test habit, adds a tracked data entry with a specific timestamp,
        and checks that the stored date is formatted correctly (YYYY-MM-DD).
        """

        # created a test Habit instance here
        habit = Habit("Test Habit", "daily", 10, 0, "Test description")
        # Then added tracked data through a sample timestamp
        habit.add_tracked_data("2022-01-01 12:00:00")
        # confirming that the date part of the tracked_data is properly stored
        self.assertEqual(habit.tracked_data[0]["date"], "2022-01-01")

    def test_get_habits_with_broken_streak(self):
        """
        For testing the get_habits_with_broken_streak function.

        Loads habit data from 'data/habits.json', converts each entry to a Habit object,
        and asserts that the function returns the expected list of habits with broken streaks.
        """
        with open('data/habits.json', 'r') as file:
            habits_data = json.load(file)
            habits = [Habit.from_dict(habit) for habit in habits_data]
            self.assertEqual(get_habits_with_broken_streak(habits),
                             ['Weekly Planning'])

    def test_get_habits_with_longest_streak(self):
        with open('data/habits.json', 'r') as file:
            habits_data = json.load(file)
            habits = [Habit.from_dict(habit) for habit in habits_data]
            self.assertEqual(get_habits_with_longest_streak(habits), ['Daily Exercise'])


if __name__ == "__main__":
    # Start the unit tests when this module is executed directly.
    unittest.main()
