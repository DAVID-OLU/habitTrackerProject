import datetime
import json
from dataclasses import dataclass, field, asdict


@dataclass
class Habit:
    name: str
    periodicity: str
    goal: int = 0
    progress: int = 0
    description: str = ""
    # The code below automatically set the creation_date variable to
    # the current date and time when a new Habit is instantiated.
    creation_date: str = field(default_factory=lambda: datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    tracked_data: list = field(default_factory=list)

    def add_tracked_data(self, completion_time: str):
        """
        This method adds a new tracked entry for the habit.

        It attempts to parse the available completion_time using the anticipated format.
        If it's successful, it appends a new dictionary to tracked_data with both the original
        completion time and a formatted date string.
        """
        try:
            # Here, I am parsing the completion_time string into a date object.
            date_obj = datetime.datetime.strptime(completion_time, "%Y-%m-%d %H:%M:%S").date()
        except ValueError:
            print(f"Invalid date format: {completion_time}")
            return

        self.tracked_data.append({
            "completion_time": completion_time,
            "date": str(date_obj)
        })

    def to_dict(self):
        """
        Converts the Habit instance into a dictionary for JSON serialization.

        This method uses asdict() to transform the dataclass into a dictionary.
        It also ensures that tracked_data is always a list of dictionaries with a string-formatted "date".

        Returns:
             dict: A dictionary representation of the Habit.
        """

        data = asdict(self)

        # Here, I am just making sure that tracked_data is a list.
        if not isinstance(data["tracked_data"], list):
            data["tracked_data"] = []

        # Then I Processed each entry in the tracked_data to make sure of appropriate formatting.
        for entry in data["tracked_data"]:
            if isinstance(entry, dict):
                entry["date"] = str(entry.get("date", ""))
            else:
                print(f"Invalid tracked_data entry found: {entry}")
                data["tracked_data"] = []

        return data

    @classmethod
    def from_dict(cls, data):
        """
        Creation of the Habit instance from a dictionary.

        This method is helpful to load habit data from the JSON file.
        It also checks that the tracked_data is correctly formatted as a list and transforms goal to an integer.

        Args:
            data (dict): A dictionary containing habit information.

        Returns:
            Habit: A newly created Habit instance from the provided data.
        """

        tracked_data = data.get("tracked_data", [])
        if isinstance(tracked_data, dict):
            tracked_data = [tracked_data]

        for i, entry in enumerate(tracked_data):
            if isinstance(entry, dict) and "date" in entry:
                entry["date"] = entry["date"]
            else:
                print(f"Invalid tracked_data entry found: {entry}")

            # Convert goal to integer
            goal = int(data.get("goal", 0))

        return cls(
            name=data["name"],
            periodicity=data["periodicity"],
            goal=data.get("goal", 0),
            progress=data.get("progress", 0),
            description=data.get("description", ""),
            creation_date=data.get("creation_date", ""),
            tracked_data=tracked_data
        )

    def is_completed(self):
        """Checks if the habit goal has been reached."""
        return self.progress >= self.goal
