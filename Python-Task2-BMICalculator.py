import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime
import matplotlib.pyplot as plt


# ============================================================
# DATABASE
# ============================================================

DATABASE_NAME = "bmi_records.db"


def create_database():
    """Create the database and BMI records table."""
    try:
        conn = sqlite3.connect(DATABASE_NAME)
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS bmi_records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                weight REAL NOT NULL,
                height REAL NOT NULL,
                bmi REAL NOT NULL,
                category TEXT NOT NULL,
                date_time TEXT NOT NULL
            )
        """)

        conn.commit()
        conn.close()

    except sqlite3.Error as e:
        messagebox.showerror(
            "Database Error",
            f"Unable to create database:\n{e}"
        )


def save_record(username, weight, height, bmi, category):
    """Save BMI record into SQLite database."""
    try:
        conn = sqlite3.connect(DATABASE_NAME)
        cursor = conn.cursor()

        date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        cursor.execute("""
            INSERT INTO bmi_records
            (username, weight, height, bmi, category, date_time)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (username, weight, height, bmi, category, date_time))

        conn.commit()
        conn.close()

        return True

    except sqlite3.Error as e:
        messagebox.showerror(
            "Database Error",
            f"Unable to save BMI record:\n{e}"
        )
        return False


def get_user_records(username):
    """Retrieve all BMI records for a user."""
    try:
        conn = sqlite3.connect(DATABASE_NAME)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT date_time, bmi, category, weight, height
            FROM bmi_records
            WHERE username = ?
            ORDER BY id ASC
        """, (username,))

        records = cursor.fetchall()

        conn.close()

        return records

    except sqlite3.Error as e:
        messagebox.showerror(
            "Database Error",
            f"Unable to read BMI records:\n{e}"
        )
        return []


# ============================================================
# BMI CALCULATION
# ============================================================

def calculate_bmi():
    """Calculate and display BMI."""

    username = username_entry.get().strip()
    weight_text = weight_entry.get().strip()
    height_text = height_entry.get().strip()

    # Validate username
    if not username:
        messagebox.showerror(
            "Input Error",
            "Please enter a username."
        )
        return

    # Validate weight
    try:
        weight = float(weight_text)
    except ValueError:
        messagebox.showerror(
            "Input Error",
            "Weight must be a numeric value."
        )
        return

    # Validate height
    try:
        height = float(height_text)
    except ValueError:
        messagebox.showerror(
            "Input Error",
            "Height must be a numeric value."
        )
        return

    # Validate positive values
    if weight <= 0:
        messagebox.showerror(
            "Input Error",
            "Weight must be greater than 0."
        )
        return

    if height <= 0:
        messagebox.showerror(
            "Input Error",
            "Height must be greater than 0."
        )
        return

    # Calculate BMI
    bmi = weight / (height ** 2)

    # Classification
    if bmi < 18.5:
        category = "Underweight"
        result_color = "blue"

    elif bmi < 25:
        category = "Normal"
        result_color = "green"

    elif bmi < 30:
        category = "Overweight"
        result_color = "orange"

    else:
        category = "Obese"
        result_color = "red"

    # Display result
    result_label.config(
        text=f"BMI: {bmi:.2f}\nCategory: {category}",
        foreground=result_color
    )

    # Save record
    saved = save_record(
        username,
        weight,
        height,
        bmi,
        category
    )

    if saved:
        messagebox.showinfo(
            "Success",
            f"BMI calculated successfully!\n\n"
            f"User: {username}\n"
            f"BMI: {bmi:.2f}\n"
            f"Category: {category}\n\n"
            f"Record saved to database."
        )

        load_history()


# ============================================================
# HISTORY
# ============================================================

def load_history():
    """Load current user's BMI history into the table."""

    username = username_entry.get().strip()

    if not username:
        messagebox.showerror(
            "Input Error",
            "Please enter a username first."
        )
        return

    # Clear old records
    for item in history_tree.get_children():
        history_tree.delete(item)

    records = get_user_records(username)

    for record in records:
        date_time, bmi, category, weight, height = record

        history_tree.insert(
            "",
            tk.END,
            values=(
                date_time,
                f"{weight:.2f}",
                f"{height:.2f}",
                f"{bmi:.2f}",
                category
            )
        )


# ============================================================
# GRAPH
# ============================================================

def show_graph():
    """Display BMI trend graph for the selected user."""

    username = username_entry.get().strip()

    if not username:
        messagebox.showerror(
            "Input Error",
            "Please enter a username first."
        )
        return

    records = get_user_records(username)

    if not records:
        messagebox.showinfo(
            "No Data",
            f"No BMI records found for {username}."
        )
        return

    dates = []
    bmi_values = []

    for record in records:
        date_time, bmi, category, weight, height = record

        dates.append(date_time)
        bmi_values.append(bmi)

    # Create graph
    plt.figure(figsize=(10, 5))

    plt.plot(
        dates,
        bmi_values,
        marker="o",
        linewidth=2
    )

    plt.axhline(
        y=18.5,
        linestyle="--",
        label="Underweight limit (18.5)"
    )

    plt.axhline(
        y=25,
        linestyle="--",
        label="Overweight limit (25)"
    )

    plt.axhline(
        y=30,
        linestyle="--",
        label="Obese limit (30)"
    )

    plt.title(f"BMI Trend - {username}")
    plt.xlabel("Date and Time")
    plt.ylabel("BMI")

    plt.xticks(
        rotation=45,
        ha="right"
    )

    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    plt.show()


# ============================================================
# CLEAR INPUTS
# ============================================================

def clear_fields():
    """Clear all input fields and result."""

    username_entry.delete(0, tk.END)
    weight_entry.delete(0, tk.END)
    height_entry.delete(0, tk.END)

    result_label.config(
        text="BMI: --\nCategory: --",
        foreground="black"
    )

    for item in history_tree.get_children():
        history_tree.delete(item)


# ============================================================
# MAIN WINDOW
# ============================================================

root = tk.Tk()

root.title("BMI Calculator")
root.geometry("850x700")
root.resizable(False, False)


# ============================================================
# TITLE
# ============================================================

title_label = ttk.Label(
    root,
    text="BMI CALCULATOR",
    font=("Arial", 24, "bold")
)

title_label.pack(pady=20)


subtitle_label = ttk.Label(
    root,
    text="Calculate, save and track your Body Mass Index",
    font=("Arial", 11)
)

subtitle_label.pack(pady=5)


# ============================================================
# INPUT FRAME
# ============================================================

input_frame = ttk.LabelFrame(
    root,
    text="User Information",
    padding=20
)

input_frame.pack(
    padx=30,
    pady=15,
    fill="x"
)


# Username
ttk.Label(
    input_frame,
    text="Username:"
).grid(
    row=0,
    column=0,
    padx=10,
    pady=10,
    sticky="w"
)

username_entry = ttk.Entry(
    input_frame,
    width=30
)

username_entry.grid(
    row=0,
    column=1,
    padx=10,
    pady=10
)


# Weight
ttk.Label(
    input_frame,
    text="Weight (kg):"
).grid(
    row=1,
    column=0,
    padx=10,
    pady=10,
    sticky="w"
)

weight_entry = ttk.Entry(
    input_frame,
    width=30
)

weight_entry.grid(
    row=1,
    column=1,
    padx=10,
    pady=10
)


# Height
ttk.Label(
    input_frame,
    text="Height (m):"
).grid(
    row=2,
    column=0,
    padx=10,
    pady=10,
    sticky="w"
)

height_entry = ttk.Entry(
    input_frame,
    width=30
)

height_entry.grid(
    row=2,
    column=1,
    padx=10,
    pady=10
)


# ============================================================
# BUTTONS
# ============================================================

button_frame = ttk.Frame(root)

button_frame.pack(pady=15)


calculate_button = ttk.Button(
    button_frame,
    text="Calculate BMI",
    command=calculate_bmi
)

calculate_button.grid(
    row=0,
    column=0,
    padx=10
)


history_button = ttk.Button(
    button_frame,
    text="Load History",
    command=load_history
)

history_button.grid(
    row=0,
    column=1,
    padx=10
)


graph_button = ttk.Button(
    button_frame,
    text="Show BMI Graph",
    command=show_graph
)

graph_button.grid(
    row=0,
    column=2,
    padx=10
)


clear_button = ttk.Button(
    button_frame,
    text="Clear",
    command=clear_fields
)

clear_button.grid(
    row=0,
    column=3,
    padx=10
)


# ============================================================
# RESULT
# ============================================================

result_frame = ttk.LabelFrame(
    root,
    text="BMI Result",
    padding=20
)

result_frame.pack(
    padx=30,
    pady=10,
    fill="x"
)


result_label = ttk.Label(
    result_frame,
    text="BMI: --\nCategory: --",
    font=("Arial", 18, "bold"),
    anchor="center"
)

result_label.pack()
history_frame = ttk.LabelFrame(
    root,
    text="BMI History",
    padding=10
)
history_frame.pack(
    padx=30,
    pady=15,
    fill="both",
    expand=True
)
columns = (
    "Date & Time",
    "Weight",
    "Height",
    "BMI",
    "Category"
)
history_tree = ttk.Treeview(
    history_frame,
    columns=columns,
    show="headings",
    height=8
)
for column in columns:
    history_tree.heading(
        column,
        text=column
    )

    history_tree.column(
        column,
        width=140,
        anchor="center"
    )
history_tree.pack(
    fill="both",
    expand=True
)
info_label = ttk.Label(
    root,
    text=(
        "BMI Categories:  "
        "Underweight < 18.5   |   "
        "Normal 18.5–24.9   |   "
        "Overweight 25–29.9   |   "
        "Obese ≥ 30"
    ),
    font=("Arial", 9)
)
info_label.pack(pady=10)
create_database()
root.mainloop()