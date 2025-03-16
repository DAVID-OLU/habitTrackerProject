import datetime
import json
import os

from completed_habits import view_completed_habits
from habit import Habit
from analytics import (
    get_all_habits,
    get_habits_by_periodicity,
    get_longest_run_streak,
    get_longest_run_streak_for_habit,
    get_habits_with_broken_streak,
    get_habits_with_longest_streak,
    check_in,
    progress_summary,
    load_completed_habits
)
from utility import save_habits, save_completed_habits
from erase import delete_habit

HABIT_FILE = "data/habits.json"


def load_habits():
    """Loads habits from a JSON file."""
    if not os.path.exists(HABIT_FILE):
        return []
    with open(HABIT_FILE, "r") as file:
        try:
            data = json.load(file)
            return [Habit.from_dict(habit) for habit in data]
        except json.JSONDecodeError:
            return []


def add_habit(habits):
    """
    Prompts the user to add a new habit and appends it to the habits list.

    The user is asked for the habit's name, periodicity (daily/weekly), description, and goal.
    The function validates the numeric input for the goal and re-prompts the user on invalid input.
    The new habit is then saved to the habits file.

    Args:
        habits (list): The list of existing Habit objects.
    """
    
    name = input("Enter the name of the new habit: ").strip()
    while True:
        periodicity = input("Enter the periodicity (daily/weekly): ").strip().lower()
        if periodicity in ["daily", "weekly"]:
            break
        else:
            print("Invalid input. Please enter either 'daily' or 'weekly'.")

    description = input("Enter the description for the habit: ").strip()

    # Validate numeric input for the goal
    while True:
        goal_input = input(f"Enter the target number of {'days' if periodicity == 'daily' else 'weeks'}: ").strip()
        try:
            goal = int(goal_input)
            break
        except ValueError:
            print("Invalid number. Please enter a valid integer for the target number.")

    new_habit = Habit(name, periodicity, goal, 0, description)
    if not hasattr(new_habit, 'creation_date') or new_habit.creation_date is None:
        new_habit.creation_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    habits.append(new_habit)
    save_habits(habits)
    print("New habit created successfully!")


def view_activities(habits):
    """
        Here, it displays the tracked activities for a chosen habit.

        but if no habits are found or the chosen habit does not have tracked data,
        appropriate messages are printed.

        Args:
            habits (list): A list of Habit objects.
        """

    if not habits:
        print("No habits found.")
        return

    print("Select a habit to view activities:")
    for i, habit in enumerate(habits, start=1):
        print(f"{i}. {habit.name}")

    try:
        choice = int(input("Enter the number of the habit: ")) - 1
        if choice < 0 or choice >= len(habits):
            print("Invalid choice.")
            return
    except ValueError:
        print("Please enter a valid number.")
        return

    selected_habit = habits[choice]
    print(f"Activities for {selected_habit.name}:")

    if not selected_habit.tracked_data:
        print("No recorded activities for this habit.")
        return

    for entry in selected_habit.tracked_data:
        if isinstance(entry, dict) and "date" in entry:
            print(f"- {entry['date']}")
        else:
            print(f"Skipping invalid entry: {entry}")


def main():
    """
    Main function for the Habit Tracker application.

    Continuously displays the menu, handles user input with validation,
    and calls appropriate functions based on the user's choice.
    """
    habits = load_habits()

    while True:
        print("\nHabit Tracker Menu\n")
        print("1. Create new habit")
        print("2. View all habits")
        print("3. View habits by periodicity")
        print("4. Get longest run streak")
        print("5. Get longest run streak for habit")
        print("6. View activities for a habit")
        print("7. Get habits with broken streak")
        print("8. Get habits with longest streak")
        print("9. Habit check-in")
        print("10. Progress insight")
        print("11. Delete habit")
        print("12. View completed habits")
        print("13. Exit\n")

        choice = input("Enter your choice: ").strip()

        # Validate that the choice is a number between 1 and 13
        if choice not in [str(i) for i in range(1, 14)]:
            print("Invalid choice. Please re-enter a number between 1 and 13.")
            continue

        if choice == "1":
            add_habit(habits)
        elif choice == "2":
            print("All Habits:")
            for habit in get_all_habits(habits):
                print(f"- {habit}")
        elif choice == "3":
            periodicity = input("Enter periodicity (daily/weekly): ").strip().lower()
            if periodicity not in ["daily", "weekly"]:
                print("Invalid periodicity. Please enter 'daily' or 'weekly'.")
                continue
            filtered_habits = get_habits_by_periodicity(habits, periodicity)
            print(f"Habits ({periodicity}):", *filtered_habits, sep="\n- ")
        elif choice == "4":
            print(f"Longest streak: {get_longest_run_streak(habits)}")
        elif choice == "5":
            while True:
                habit_name = input("Enter habit name: ").strip()
                if not habit_name:
                    print("Habit name cannot be empty. Please try again.")
                    continue
                if habit_name.isdigit():
                    print("Invalid input, enter a valid habit name (non-numeric).")
                elif not any(habit.name.lower() == habit_name.lower() for habit in habits):
                    print(f"Habit '{habit_name}' not found. Please try again.")
                else:
                    for habit in habits:
                        if habit.name.lower() == habit_name.lower():
                            print(
                                f"Longest streak for '{habit.name}': {get_longest_run_streak_for_habit(habits, habit.name)}"
                            )
                            break
                    break
        elif choice == "6":
            view_activities(habits)
        elif choice == "7":
            print("Broken streak habits:", *get_habits_with_broken_streak(habits), sep="\n- ")
        elif choice == "8":
            print("Habits with active longest streak:", *get_habits_with_longest_streak(habits), sep="\n- ")
        elif choice == "9":
            habit_name = input("Enter habit name: ").strip()
            if not habit_name:
                print("Your habit name cannot be left empty.")
                continue
            completed_input = input("Did you complete this habit today? (yes/no): ").strip().lower()
            if completed_input not in ["yes", "no"]:
                print("Invalid input for completion. Please enter 'yes' or 'no'.")
                continue
            completed = completed_input == "yes"  # Convert input to boolean
            for habit in habits:
                if habit.name.lower() == habit_name.lower():
                    check_in(habits, habit.name, completed)
                    break
            else:
                print(f"Habit '{habit_name}' not found.")
        elif choice == "10":
            print(progress_summary(habits))
        elif choice == "11":
            delete_habit(habits)
        elif choice == "12":
            view_completed_habits(load_completed_habits())
        elif choice == "13":
            print("Exited goodbye...")
            break


if __name__ == "__main__":
    main()

