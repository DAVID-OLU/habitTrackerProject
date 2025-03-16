"""
This a Unit tests for the Habit class in the Habit Tracker project.

This module consists test scenarios for making Habit objects, their progress update,
tracking data, converting to/from dictionary representations, and then the loading of habits from a file.
"""

import unittest
from habit import Habit
from datetime import datetime
import json


class TestHabit(unittest.TestCase):
    """
    Test suite for Habit tracked data functionality.
    """

    def test_habit_creation(self):
        """
        Test that a Habit object is created with the appropriate attributes.

        Validates that the habit name, periodicity, goal, progress, and description match anticipated values.
        """
        habit = Habit("Test Habit", "daily", 10, 0, "Test description")
        self.assertEqual(habit.name, "Test Habit")
        self.assertEqual(habit.periodicity, "daily")
        self.assertEqual(habit.goal, 10)
        self.assertEqual(habit.progress, 0)
        self.assertEqual(habit.description, "Test description")

    def test_habit_progress(self):
        """
        Test that the progress of Habit object can be updated correctly.
        """
        habit = Habit("Test Habit", "daily", 10, 0, "Test description")
        habit.progress = 5
        self.assertEqual(habit.progress, 5)

    def test_habit_is_completed(self):
        """
        Test that when the habit's progress meets goal, the is_completed method returns True  or exceeds the goal.
        """
        habit = Habit("Test Habit", "daily", 10, 10, "Test description")
        self.assertTrue(habit.is_completed())

    def test_habit_add_tracked_data(self):
        """
        Test the add_tracked_data method for adding a new tracked entry.

        It validates that the tracked_data list's length increases, after adding a tracked data entry.
        """
        habit = Habit("Test Habit", "daily", 10, 0, "Test description")
        habit.add_tracked_data("2022-01-01 12:00:00")
        self.assertEqual(len(habit.tracked_data), 1)

    def test_habit_to_dict(self):
        """
        Test the to_dict method of the Habit class.

        Validates that the returned dictionary consists the correct values for name, periodicity,
        goal, progress, and description.
        """
        habit = Habit("Test Habit", "daily", 10, 0, "Test description")
        habit_dict = habit.to_dict()
        self.assertEqual(habit_dict["name"], "Test Habit")
        self.assertEqual(habit_dict["periodicity"], "daily")
        self.assertEqual(habit_dict["goal"], 10)
        self.assertEqual(habit_dict["progress"], 0)
        self.assertEqual(habit_dict["description"], "Test description")

    def test_habit_from_dict(self):
        """
        Test the from_dict class method for creating a Habit object from a dictionary.

        Guarantees that the Habit created from the dictionary has the expected attribute values.
        """
        habit_dict = {
            "name": "Test Habit",
            "periodicity": "daily",
            "goal": 10,
            "progress": 0,
            "description": "Test description",
            "tracked_data": []
        }
        habit = Habit.from_dict(habit_dict)
        self.assertEqual(habit.name, "Test Habit")
        self.assertEqual(habit.periodicity, "daily")
        self.assertEqual(habit.goal, 10)
        self.assertEqual(habit.progress, 0)
        self.assertEqual(habit.description, "Test description")


class TestHabitTrackedData(unittest.TestCase):
    """
    Habit tracked data functionality test suite.
    """

    def test_habit_tracked_data(self):
        """
        Test that adding multiple tracked data entries appropriately updates the length of the tracked_data list.
        """
        habit = Habit("Test Habit", "daily", 10, 0, "Test description")
        habit.add_tracked_data("2022-01-01 12:00:00")
        habit.add_tracked_data("2022-01-02 12:00:00")
        self.assertEqual(len(habit.tracked_data), 2)

    def test_habit_tracked_data_date(self):
        """
        Test that the date component of tracked data is stored in the correct format.

        After adding tracked data, it confirms that the 'date' field in the first entry is formatted as 'YYYY-MM-DD'.
        """
        habit = Habit("Test Habit", "daily", 10, 0, "Test description")
        habit.add_tracked_data("2022-01-01 12:00:00")
        self.assertEqual(habit.tracked_data[0]["date"], "2022-01-01")


class TestHabitFromFile(unittest.TestCase):
    """
    Test suite for creating Habit objects from file data.
    """

    def test_habit_from_file(self):
        with open('data/habits.json', 'r') as file:
            habits_data = json.load(file)
            habit = Habit.from_dict(habits_data[0])
            self.assertEqual(habit.name, "Daily Exercise")
            self.assertEqual(habit.periodicity, "daily")
            self.assertEqual(habit.goal, 60)
            self.assertEqual(habit.progress, 40)
            self.assertEqual(habit.description, "Exercise for 30 minutes")


if __name__ == "__main__":
    unittest.main()
