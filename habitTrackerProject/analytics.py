import datetime
import os
from habit import Habit
import json
from datetime import timedelta

from utility import save_habits


def get_all_habits(habits):
    """
    It gets the names of all habits.

    Args:
        habits (list): A list of Habit objects.

    Returns:
        list: This is the list consisting of the names of all habits.
    """
    return [habit.name for habit in habits]


def get_habits_by_periodicity(habits, periodicity):
    """
    It refines habits based on their periodicity.

    Args:
        habits (list): A list of Habit objects.
        periodicity (str): The periodicity to filter or group by (e.g., "daily" or "weekly").

    Returns:
        list: The list of the habit names that align with the defined periodicity.
    """
    return [habit.name for habit in habits if habit.periodicity == periodicity]


def get_longest_run_streak(habits):
    """
    Calculates the longest active consecutive run streak across all habits.
    Only the streaks that are still active (i.e, the most recent check-in is within
    the expected interval relative to today) are considered or counted.

    Args:
        habits (list): A list of Habit objects.

    Returns:
        int: The overall longest active streak found across all habits.
    """
    longest_streak = 0
    today = datetime.datetime.now().date()

    for habit in habits:
        allowed_gap = get_days(habit.periodicity)
        if not habit.tracked_data:
            continue

        # Convert the tracked date strings to date objects.
        dates = []
        for entry in habit.tracked_data:
            try:
                date_obj = datetime.datetime.strptime(entry["date"], "%Y-%m-%d %H:%M:%S").date()
            except ValueError:
                date_obj = datetime.datetime.strptime(entry["date"], "%Y-%m-%d").date()
            dates.append(date_obj)
        dates.sort()

        # Calculate the consecutive streak based on allowed_gap.
        streak = 1
        for i in range(1, len(dates)):
            if (dates[i] - dates[i - 1]).days == allowed_gap:
                streak += 1
            else:
                streak = 1

        # Verify if the streak is still active.
        # If the gap from the last check-in to today is too large, the active streak is reset to 0.
        if (today - dates[-1]).days > allowed_gap:
            streak = 0

        longest_streak = max(longest_streak, streak)

    return longest_streak


def get_longest_run_streak_for_habit(habits, habit_name):
    """
    Computes the active consecutive run streak for a specific habit.
    Only counts the streak if the most recent check-in is within the expected interval relative to today.

    Args:
        habits (list): List of Habit objects.
        habit_name (str): Name of the habit to compute the streak for.

    Returns:
        int: The active streak for the specified habit, or 0 if not found or not active.
    """
    today = datetime.datetime.now().date()

    for habit in habits:
        if habit.name.lower() == habit_name.lower():
            allowed_gap = get_days(habit.periodicity)
            if not habit.tracked_data:
                return 0

            dates = []
            for entry in habit.tracked_data:
                try:
                    date_obj = datetime.datetime.strptime(entry["date"], "%Y-%m-%d %H:%M:%S").date()
                except ValueError:
                    date_obj = datetime.datetime.strptime(entry["date"], "%Y-%m-%d").date()
                dates.append(date_obj)
            dates.sort()

            streak = 1
            for i in range(1, len(dates)):
                if (dates[i] - dates[i - 1]).days == allowed_gap:
                    streak += 1
                else:
                    streak = 1

            if (today - dates[-1]).days > allowed_gap:
                return 0
            return streak

    return 0


def get_days(periodicity):
    if periodicity == "daily":
        return 1
    elif periodicity == "weekly":
        return 7
    else:
        raise ValueError("Invalid periodicity")


def get_habits_with_broken_streak(habits):
    """
    Returns the list of habit names that have a broken streak.

    A streak will be considered as broken if the number of days since the last check-in of that habit
    exceeds the habit's periodicity.

    Args:
        habits (list): A list of habit objects.

    Returns:
        list: A list of habit names with broken streaks.
    """

    # Initialize an empty list to store habits with broken streaks
    habits_with_broken_streak = []

    # Get today's date
    today = datetime.datetime.now().date()

    # Iterated over each of the habit
    for habit in habits:

        # then check if the habit has any tracked data
        if habit.tracked_data:
            dates = []

            # Iterated over each entry in the tracked data
            for entry in habit.tracked_data:
                date_str = entry["date"]

                if " " in date_str:
                    # Parse the date string with time
                    date_obj = datetime.datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S").date()
                else:
                    date_obj = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()

                # Added the parsed date to the list of dates
                dates.append(date_obj)

            # Sort the list of dates in ascending order
            dates.sort()
            # Then I compared today's date with the last check-in date
            if (today - dates[-1]).days > get_days(habit.periodicity):
                # so if the streak is broken, add the name of the habit to the list
                habits_with_broken_streak.append(habit.name)

    return habits_with_broken_streak


def get_habits_with_longest_streak(habits: list[Habit]) -> list[str]:
    """
    Returns a list of habit names that have the longest streak.

    A streak is considered as the longest if it equals the overall longest streak
    among all habits.

    Args:
        habits (list): A list of habit objects.

    Returns:
        list: A list of habit names with the longest streak.
    """

    # first fetch the overall longest streak among all habits
    overall_longest = get_longest_run_streak(habits)

    habits_with_longest = []
    # fetch today's current date
    today = datetime.datetime.now().date()

    # Iterated over each of the habit
    for habit in habits:

        # Get the allowed interval gap in days based on the habit's periodicity
        allowed_interval_gap = get_days(habit.periodicity)
        if not habit.tracked_data:
            continue

        # Parse and sort the dates of that tracked data
        dates = []

        for entry in habit.tracked_data:
            try:
                # Trying to parse the date string with time
                date_obj = datetime.datetime.strptime(entry["date"], "%Y-%m-%d %H:%M:%S").date()
            except ValueError:

                # But if it fails, then try to parse the date string without time
                date_obj = datetime.datetime.strptime(entry["date"], "%Y-%m-%d").date()
            dates.append(date_obj)
        dates.sort()

        # Evaluate the active streak for this habit.
        streak = 1
        for i in range(1, len(dates)):

            # Confirm if the gap between that consecutive dates is equal to the allowed interval gap
            if (dates[i] - dates[i - 1]).days == allowed_interval_gap:
                streak += 1
            else:
                streak = 1

        # Confirming if the streak is still currently active
        if (today - dates[-1]).days > allowed_interval_gap:
            streak = 0

        # Then again, check if this evaluated active streak equals the overall longest
        if streak == overall_longest and streak != 0:
            # If it is, then add the habit name to the list
            habits_with_longest.append(habit.name)

    # Returning the list of habits containing the longest streak
    return habits_with_longest


def check_in(habits, habit_name, completed):
    """
        Check-in a habit and then updates the tracked data.

        Args:
            habits (list): A list of Habit objects.
            habit_name (str): The name of the habit to check in.
            completed (bool): Whether the habit has been completed.

        Returns:
            None

        Notes:
            This function checks if the habit has already been checked in for the day or week, depending on
            the habit's periodicity.
            If the habit has been completed, it is added to the list of completed habits and removed from the
            list of active habits.
        """
    for habit in habits:
        if habit.name == habit_name:
            # retrieve current timestamp for the check-in.
            today = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # Checking if the habit has already been checked-in today (for daily habits)
            # or this week (for weekly habits periodicity).
            if habit.tracked_data:
                tracked_dates = [entry["date"] for entry in habit.tracked_data]

                if habit.periodicity == "daily":
                    today_date = datetime.datetime.now().strftime("%Y-%m-%d")
                    tracked_dates_daily = [entry["date"].split(" ")[0] for entry in habit.tracked_data]
                    if today_date in tracked_dates_daily:
                        print("You have already checked in for today.")
                        return

                elif habit.periodicity == "weekly":
                    today_date = datetime.datetime.now().strftime("%Y-%m-%d")
                    tracked_dates_weekly = [entry["date"].split(" ")[0] for entry in habit.tracked_data]

                    # Decide the week number for each tracked date.
                    tracked_weeks = [datetime.datetime.strptime(date, "%Y-%m-%d").isocalendar()[1] for date in
                                     tracked_dates_weekly]
                    current_week = datetime.datetime.now().isocalendar()[1]

                    if current_week in tracked_weeks:
                        print("You have already checked in for this week.")
                        return

            # today's check-in is appended to the habit's tracked data.
            habit.tracked_data.append({"date": today})

            # And if the habit is marked as finished, update progress and check for goal completion.
            if completed:
                habit.progress += 1
                if habit.is_completed():
                    print(f"Congratulations! You have completed the habit '{habit_name}'!")
                    completed_habits = load_completed_habits()
                    completed_habit = Habit(
                        name=habit.name,
                        periodicity=habit.periodicity,
                        goal=habit.goal,
                        progress=habit.progress,
                        description=habit.description,
                        creation_date=habit.creation_date,
                        tracked_data=habit.tracked_data
                    )
                    completed_habits.append(completed_habit)
                    save_completed_habits(completed_habits)

                    # Here, the code removes the completed habit from the active list and save the changes.
                    habits.remove(habit)
                    save_habits(habits)
                    print("Check-in successful!")
                    return

            save_habits(habits)
            print("Check-in successful!")
            return
    print("Habit not found.")


def progress_summary(habits):
    """
    Produces a summary of progress for each habit.

    Args:
        habits (list): A list of Habit objects.

    Returns:
        str: A multi-line string summarizing each habit's name, goal, description, and progress.
    """

    summary = []
    for habit in habits:
        summary.append(
            f"Habit: {habit.name}, Goal: {habit.goal}, Description: {habit.description}, Progress: {habit.progress}/{habit.goal}")
    return "\n".join(summary)


def load_completed_habits():
    """
    completed habits from the JSON file is loaded.

    Returns:
        list: A list of Habit objects loaded from the completed habits file.
            Returns an empty list if the file is not found.
    """

    try:
        with open("data/completed_habits.json", "r") as file:
            data = json.load(file)
            return [Habit.from_dict(habit) for habit in data]
    except FileNotFoundError:
        return []


def save_completed_habits(completed_habits):
    """
    The list of completed habits is saved to a JSON file.

    Ensures the data directory exists before writing to the file.

    Args:
        completed_habits (list): A list of Habit objects representing completed habits.
    """

    data_dir = "data"
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

    file_path = os.path.join(data_dir, "completed_habits.json")
    data = [habit.to_dict() for habit in completed_habits]
    with open(file_path, "w") as file:
        json.dump(data, file, indent=4)
