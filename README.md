# Python Programming Tasks

This repository contains three Python projects developed as part of Python programming practice/internship tasks:

1. Voice Assistant
2. BMI Calculator
3. Random Password Generator

## Projects

### 1. Voice Assistant

A simple voice-controlled assistant that listens to spoken commands and responds using text-to-speech.

#### Features
- Greets the user.
- Recognizes voice commands.
- Tells the current time.
- Tells the current date.
- Performs Google searches in a web browser.
- Handles unrecognized speech.
- Exits when the user says `exit`, `quit`, or `stop`.

#### Technologies Used
- Python
- `speech_recognition`
- `pyttsx3`
- `datetime`
- `webbrowser`

#### Installation

Install the required packages:

```bash
pip install SpeechRecognition pyttsx3 PyAudio
```

> Note: Microphone access and a working audio setup are required.

#### Run the Project

```bash
python "Python-TASK 1 · Voice Assistant.py"
```

---

### 2. BMI Calculator

A graphical BMI Calculator built with Tkinter. It calculates Body Mass Index, classifies the result, stores records in an SQLite database, and displays BMI history and trends.

#### Features
- Accepts username, weight, and height.
- Calculates BMI using the formula:

  `BMI = weight / (height²)`

- Displays BMI categories:
  - Underweight: BMI below 18.5
  - Normal: BMI from 18.5 to below 25
  - Overweight: BMI from 25 to below 30
  - Obese: BMI 30 or above
- Saves BMI records in an SQLite database.
- Loads a user's BMI history.
- Displays a BMI trend graph.
- Provides a button to clear input fields and results.
- Validates user input.

#### Technologies Used
- Python
- Tkinter
- SQLite3
- Matplotlib
- `datetime`

#### Installation

Install Matplotlib:

```bash
pip install matplotlib
```

> Tkinter and SQLite3 are commonly included with standard Python installations. Availability may depend on the operating system.

#### Run the Project

```bash
python Python-Task2-BMICalculator.py
```

The application automatically creates a database file named `bmi_records.db` in the project folder.

---

### 3. Random Password Generator

A graphical password generator that creates random passwords using selected character types and securely copies them to the clipboard.

#### Features
- Generates passwords between 8 and 64 characters.
- Supports:
  - Uppercase letters
  - Lowercase letters
  - Numbers
  - Symbols
- Requires at least two character types.
- Allows ambiguous characters such as `0`, `O`, `l`, and `1` to be excluded.
- Displays an estimated password strength:
  - Weak
  - Medium
  - Strong
- Automatically copies generated passwords to the clipboard.
- Provides a button to copy passwords manually.
- Stores the last five generated passwords in the application history.

#### Technologies Used
- Python
- Tkinter
- `secrets`
- `string`
- `pyperclip`

#### Installation

Install the clipboard package:

```bash
pip install pyperclip
```

#### Run the Project

```bash
python "Python-TASK 3 · Random Password Generator.py"
```

---

## Requirements

- Python 3.x
- A working Python development environment, such as VS Code or PyCharm
- Required packages installed for each project
- Microphone access for the Voice Assistant

## How to Use This Repository

1. Clone the repository:

   ```bash
   git clone <your-repository-url>
   ```

2. Open the project folder in VS Code or another Python editor.
3. Install the required dependencies.
4. Run any of the Python files using the commands provided above.

## Learning Outcomes

By completing these projects, the following concepts are practiced:

- Python functions and conditional statements
- Loops and user input validation
- Object-oriented programming
- GUI development with Tkinter
- Speech recognition and text-to-speech
- File and database handling
- Data visualization using Matplotlib
- Secure random password generation
- Clipboard operations
- Exception handling

## Author

**Syed Khaja Mohiddin**

B.Tech – Computer Science and Engineering
