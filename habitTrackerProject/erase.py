"""
This module for deleting a habit.

It offers functionality to show the list of current habits,
then permit the user to choose one by its number for deletion, confirm the deletion again,
and then remove the habit from the list of active habits and at the same time saving the updated list.
"""

from habit import Habit
import json
from utility import save_habits


def delete_habit(habits):
    """
    Removes/deletes a chosen habit from the list of current active habits.

    This function performs the steps at follows:
        1. Checks if there are any habits available.
        2. Outputs a numbered list of habits and prompts the user to choose one.
        3. Verifies the user's input to ensure it is a valid number.
        4. Asks user for confirmation before deleting the chosen habit.
        5. If confirmed, habit is removed from the list and saves the updated list.
             if not confirmed, the deletion process is cancelled.

    Args:
        habits (list): list of Habit objects identifying the active habits.

    Returns:
        None
    """

    # Check if there are any habits to delete
    if not habits:
        print("No habits available.")
        return

    # I looped until a correct habit number is provided - input validation
    while True:
        try:
            print("Select a habit to delete:")
            # Outputs each of the habit with its correlating number
            for i, habit in enumerate(habits):
                print(f"{i + 1}. {habit.name}")

            # Asks the user to input habit number and then it convert input to index
            choice = int(input("Enter the number of the habit: ")) - 1
            if choice < 0 or choice >= len(habits):
                print("Invalid choice. Please try again.")
            else:
                break
        # Handles error
        except ValueError:
            print("Invalid input. Please enter a number.")

    # get the habit that's correlating to the valid choice
    habit = habits[choice]

    # Confirm user deletion
    while True:
        confirm = input(f"Are you sure you want to delete the habit '{habit.name}'? (yes/no): ").strip().lower()
        if confirm in ["yes", "no"]:
            break
        else:
            print("Please enter either 'yes' or 'no'.")

    # If the deletion is confirmed, remove the habit and then save the updated list
    if confirm == "yes":
        habits.remove(habit)
        save_habits(habits)
        print(f"The habit '{habit.name}' has been deleted successfully!")
    else:
        print("Deletion cancelled.")
