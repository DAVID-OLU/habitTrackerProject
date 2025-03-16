from analytics import load_completed_habits


def view_completed_habits(completed_habits):
    """
    It shows the list of all completed habits.

    Args:
        completed_habits (list): A list of Habit objects that have been completed.

    Behavior:
         If there are no habits that are completed, prints an appropriate message.
        else, then it prints a numbered list of the completed habit names.
    """

    if not completed_habits:
        print("No completed habits available.")
        return

    print("Completed Habits:")
    # Go over all the completed habits and show each with a number.
    for i, habit in enumerate(completed_habits):
        print(f"{i + 1}. {habit.name}")


def main():
    """
    This is the main function used for viewing all completed habits.

    get the list of the completed habits from the analytics module using
    load_completed_habits(), and then calls view_completed_habits() to output them.
    """
    completed_habits = load_completed_habits()
    view_completed_habits(completed_habits)
