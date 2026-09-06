import tkinter as tk
from tkinter import messagebox
import secrets
import string
import pyperclip


# Character sets
CHARACTERS = {
    "Uppercase": string.ascii_uppercase,
    "Lowercase": string.ascii_lowercase,
    "Numbers": string.digits,
    "Symbols": string.punctuation
}

AMBIGUOUS = "0Ol1"


class PasswordGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Random Password Generator")
        self.root.geometry("500x650")
        self.root.resizable(False, False)

        self.history = []

        # Title
        tk.Label(
            root,
            text="🔐 Random Password Generator",
            font=("Arial", 20, "bold")
        ).pack(pady=15)

        # Length
        tk.Label(
            root,
            text="Password Length:",
            font=("Arial", 12)
        ).pack()

        self.length = tk.IntVar(value=12)

        tk.Spinbox(
            root,
            from_=8,
            to=64,
            textvariable=self.length,
            width=10,
            font=("Arial", 12)
        ).pack(pady=5)

        # Character type checkboxes
        tk.Label(
            root,
            text="Select Character Types:",
            font=("Arial", 12, "bold")
        ).pack(pady=(15, 5))

        self.uppercase = tk.BooleanVar(value=True)
        self.lowercase = tk.BooleanVar(value=True)
        self.numbers = tk.BooleanVar(value=True)
        self.symbols = tk.BooleanVar(value=True)

        tk.Checkbutton(
            root,
            text="Uppercase Letters (A-Z)",
            variable=self.uppercase
        ).pack(anchor="w", padx=120)

        tk.Checkbutton(
            root,
            text="Lowercase Letters (a-z)",
            variable=self.lowercase
        ).pack(anchor="w", padx=120)

        tk.Checkbutton(
            root,
            text="Numbers (0-9)",
            variable=self.numbers
        ).pack(anchor="w", padx=120)

        tk.Checkbutton(
            root,
            text="Symbols (!@#$...)",
            variable=self.symbols
        ).pack(anchor="w", padx=120)

        # Ambiguous characters
        self.exclude_ambiguous = tk.BooleanVar(value=False)

        tk.Checkbutton(
            root,
            text="Exclude ambiguous characters (0, O, l, 1)",
            variable=self.exclude_ambiguous
        ).pack(pady=10)

        # Password display
        tk.Label(
            root,
            text="Generated Password:",
            font=("Arial", 12, "bold")
        ).pack(pady=(10, 5))

        self.password_var = tk.StringVar()

        self.password_entry = tk.Entry(
            root,
            textvariable=self.password_var,
            font=("Arial", 14),
            justify="center",
            width=35
        )
        self.password_entry.pack(pady=5)

        # Strength
        self.strength_label = tk.Label(
            root,
            text="Strength: -",
            font=("Arial", 12, "bold")
        )
        self.strength_label.pack(pady=10)

        # Buttons
        tk.Button(
            root,
            text="Generate Password",
            command=self.generate_password,
            font=("Arial", 12, "bold"),
            width=20
        ).pack(pady=5)

        tk.Button(
            root,
            text="Copy to Clipboard",
            command=self.copy_password,
            font=("Arial", 11),
            width=20
        ).pack(pady=5)

        # History
        tk.Label(
            root,
            text="Last 5 Generated Passwords",
            font=("Arial", 12, "bold")
        ).pack(pady=(15, 5))

        self.history_list = tk.Listbox(
            root,
            width=50,
            height=7,
            font=("Courier", 10)
        )
        self.history_list.pack()

        # Generate first password
        self.generate_password()

    def get_selected_types(self):
        selected = []

        if self.uppercase.get():
            selected.append("Uppercase")

        if self.lowercase.get():
            selected.append("Lowercase")

        if self.numbers.get():
            selected.append("Numbers")

        if self.symbols.get():
            selected.append("Symbols")

        return selected

    def generate_password(self):
        try:
            length = int(self.length.get())
        except ValueError:
            messagebox.showerror(
                "Invalid Length",
                "Please enter a valid password length."
            )
            return

        if length < 8:
            messagebox.showerror(
                "Invalid Length",
                "Password length must be at least 8 characters."
            )
            return

        selected_types = self.get_selected_types()

        if len(selected_types) < 2:
            messagebox.showerror(
                "Invalid Selection",
                "Please select at least 2 character types."
            )
            return

        # Create character pool
        pool = ""

        for character_type in selected_types:
            pool += CHARACTERS[character_type]

        # Remove ambiguous characters if requested
        if self.exclude_ambiguous.get():
            pool = "".join(
                char for char in pool
                if char not in AMBIGUOUS
            )

        # Make sure every selected type is represented
        password_chars = []

        for character_type in selected_types:
            characters = CHARACTERS[character_type]

            if self.exclude_ambiguous.get():
                characters = "".join(
                    char for char in characters
                    if char not in AMBIGUOUS
                )

            password_chars.append(
                secrets.choice(characters)
            )

        # Fill remaining positions
        while len(password_chars) < length:
            password_chars.append(
                secrets.choice(pool)
            )

        # Secure shuffle
        for i in range(len(password_chars) - 1, 0, -1):
            j = secrets.randbelow(i + 1)
            password_chars[i], password_chars[j] = (
                password_chars[j],
                password_chars[i]
            )

        password = "".join(password_chars)

        self.password_var.set(password)

        # Update strength
        self.calculate_strength(length, len(selected_types))

        # Automatically copy password
        self.copy_password(show_message=False)

        # Add to history
        self.history.insert(0, password)

        # Keep only last 5
        self.history = self.history[:5]

        self.history_list.delete(0, tk.END)

        for item in self.history:
            self.history_list.insert(tk.END, item)

    def calculate_strength(self, length, diversity):
        score = 0

        if length >= 12:
            score += 2
        elif length >= 8:
            score += 1

        if diversity >= 3:
            score += 2
        elif diversity == 2:
            score += 1

        if length >= 16:
            score += 1

        if score <= 2:
            strength = "Weak"
        elif score <= 4:
            strength = "Medium"
        else:
            strength = "Strong"

        self.strength_label.config(
            text=f"Strength: {strength}"
        )

    def copy_password(self, show_message=True):
        password = self.password_var.get()

        if not password:
            messagebox.showwarning(
                "No Password",
                "Generate a password first."
            )
            return

        pyperclip.copy(password)

        if show_message:
            messagebox.showinfo(
                "Copied",
                "Password copied to clipboard!"
            )


# Start application
root = tk.Tk()
app = PasswordGenerator(root)
root.mainloop()