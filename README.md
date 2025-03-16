
# Habit Tracker – Command-Line Python Application

The Habit Tracker app is a command-line Python application developed to assist users build positive habits and track their progress over time. This program enable users to create daily or weekly habits, check-in habit completions, track their habit streaks, identify broken streaks, view summaries, and analyze their consistency through habit analytics. It is designed using Python’s standard libraries and implements a modular architecture that is simple to understand, maintain, and upgrade.





## Installation

-  To get started with the Habit Tracker application, clone the repository to your local machine using the following command in your terminal or command prompt:

```bash
  git clone https://github.com/DAVID-OLU/habitTrackerProject.git

```

-  After cloning the repository, navigate into the project directory:
```bash
  cd habitTrackerProject
```

-  Ensure that you are using Python 3.7 or above. You can verify your Python version by running:
```bash
  python --version
```

-  No external libraries need to be installed, so you can directly run the application using the command:
```bash
  python main.py
```


## Features

-  Creation of new habits with customized goals and periodicity.

-  Checking of progress each day or week.

-  Users can view all existing habits and also based on their periodicity.

-  Users can inspect the habit's activity logs.

-  User can analyze longest streaks and broken streaks.

-  Users can check the longest run streak for a particular habit.

-  Users can check the longest run streak.

-  Generate progress insight summaries.

-  The application automatically moves completed habits to a separate archive and allows users to view their accomplished goals.

-  Users can delete their habits.



## Project Structure

The project is organized into several Python files, each responsible for a specific functionality. The main.py file acts as the entry point of the application and provides an interactive menu-like interface. The habit.py file defines the core Habit class using Python dataclasses. 

The analytics.py file contains all the logic for analyzing habit streaks and performance metrics. The utility.py file handles the file reading and writing functionality. 

Additional modules such as erase.py and completed_habits.py manages the habit deletion and completed habit display respectively. The project also includes a test suite, with files like test_habit.py and test_analytics.py encompasses unit tests for the validation of the habit management features and the analytic functionalities.





## How to Use the Application

Once the application is running, you will see an interactive menu in your terminal. You can choose from the list of options by entering the corresponding number. You can create a new habit, log daily or weekly progress, check your longest streaks, view habit activities, identify broken streaks, generate insight summaries, delete existing habits, or view your completed habit list.

When creating a new habit, the system will prompt you to enter the habit name, the periodicity (daily or weekly), a description, and your target goal. All the data entered will be saved in habits.json located in the /data directory.

In order to track your progress, choose the 'Habit check-in' option in the menu and enter the name of the habit you wish to check-in. After then answer the confirmatory question (yes or no) and based on your answer, the system will proceed. If you answer 'yes', application will log the current date and update your progress. Once a habit reaches its goal, it is automatically transferred to the completed habits file, and then you can view it anytime via the corresponding menu option.

All the habit activities and progress summaries are displayed directly in the terminal for simplicity and ease of access.
## Unit Tests

The project includes unit tests to ensure the application works reliably. To run the tests, simply execute the following command in the project root directory:
```bash
  python -m unittest discover -s tests
```
This will automatically discover and run all test files located in the directory, including test_habit.py and test_analytics.py.

## Tech Stack

**Development Enviroment:** PyCharm IDE, Terminal

**Language:** Python


## Reference Links

draw.io - (https://app.diagrams.net/)

JetBrains. (2024). PyCharm: The Python IDE for Professional Developers. Retrieved from https://www.jetbrains.com/pycharm/

Python Software Foundation. (2024). The Python language reference (Version 3.x). Retrieved from https://docs.python.org/3/

Python Software Foundation. (2024). json — JSON encoder and decoder. Retrieved from https://docs.python.org/3/library/json.html

Python Software Foundation. (2024). dataclasses — Data classes. Retrieved from https://docs.python.org/3/library/dataclasses.html

Python Software Foundation. (2024). unittest — Unit testing framework. Retrieved from https://docs.python.org/3/library/unittest.html


