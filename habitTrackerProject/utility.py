import json
import os


def save_habits(habits):
    """
    The function saves the list of active habits to a JSON file.

    It converts each Habit object to a dictionary using the to_dict() method,
    and then writes the proceeding list to 'data/habits.json'. However, if the 'data' directory does not exist,
    it will be created.

    Args:
        habits (list): list of Habit objects representing active habits.
    """
    data_dir = "data"
    # produce the data directory if it does not exist
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

    # Set up the file path for the habits file
    file_path = os.path.join(data_dir, "habits.json")

    # Then changing each habit object to a dictionary
    data = [habit.to_dict() for habit in habits]
    # Opening the file and then writing the JSON data with indentation for the purpose of readability
    with open(file_path, "w") as file:
        json.dump(data, file, indent=4)


def save_completed_habits(completed_habits):
    """
    It saves the list of the completed habits to a JSON file.

    This function converts each completed Habit object to a dictionary using the to_dict() method,
    and then writes the resulting list to 'data/completed_habits.json'. If the 'data' directory does not exist,
    it will be created.

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
