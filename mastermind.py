import tkinter as tk
from tkinter import messagebox
import random

COLORS = ['Red', 'Green', 'Blue', 'Yellow', 'Orange', 'Purple']
CODE_LENGTH = 4
MAX_ATTEMPTS = 10

class MastermindGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Mastermind Game")
        self.secret_code = random.choices(COLORS, k=CODE_LENGTH)
        self.current_guess = []
        self.attempts = 0

        self.create_widgets()

    def create_widgets(self):
    
        tk.Label(self.root, text="Select 4 colors to make your guess:", font=('Arial', 12)).pack(pady=10)

        
        button_frame = tk.Frame(self.root)
        button_frame.pack()
        for color in COLORS:
            btn = tk.Button(button_frame, text=color, bg=color.lower(), fg='white', width=10,
                            command=lambda c=color: self.select_color(c))
            btn.pack(side=tk.LEFT, padx=5)

        self.guess_label = tk.Label(self.root, text="Current Guess: ", font=('Arial', 12))
        self.guess_label.pack(pady=10)

        self.submit_button = tk.Button(self.root, text="Submit Guess", command=self.check_guess, state=tk.DISABLED)
        self.submit_button.pack(pady=10)

        self.feedback_frame = tk.Frame(self.root)
        self.feedback_frame.pack(pady=10)

    def select_color(self, color):
        if len(self.current_guess) < CODE_LENGTH:
            self.current_guess.append(color)
            self.update_guess_label()

        if len(self.current_guess) == CODE_LENGTH:
            self.submit_button.config(state=tk.NORMAL)

    def update_guess_label(self):
        self.guess_label.config(text="Current Guess: " + " | ".join(self.current_guess))

    def check_guess(self):
        black, white = self.get_feedback(self.secret_code, self.current_guess)
        feedback_text = f"Attempt {self.attempts+1}: {' | '.join(self.current_guess)} → ⚫ {black} | ⚪ {white}"
        tk.Label(self.feedback_frame, text=feedback_text).pack(anchor='w')

        self.attempts += 1

        if black == CODE_LENGTH:
            messagebox.showinfo("Congratulations!", f"You cracked the code in {self.attempts} attempts!")
            self.root.quit()
        elif self.attempts >= MAX_ATTEMPTS:
            messagebox.showinfo("Game Over", f"Out of attempts! The correct code was: {' | '.join(self.secret_code)}")
            self.root.quit()

        self.current_guess = []
        self.update_guess_label()
        self.submit_button.config(state=tk.DISABLED)

    def get_feedback(self, code, guess):
        black_pegs = 0
        white_pegs = 0

        code_copy = code[:]
        guess_copy = guess[:]

        
        for i in range(CODE_LENGTH):
            if guess[i] == code[i]:
                black_pegs += 1
                code_copy[i] = None
                guess_copy[i] = None

        for i in range(CODE_LENGTH):
            if guess_copy[i] and guess_copy[i] in code_copy:
                white_pegs += 1
                code_index = code_copy.index(guess_copy[i])
                code_copy[code_index] = None

        return black_pegs, white_pegs


if __name__ == "__main__":
    root = tk.Tk()
    game = MastermindGame(root)
    root.mainloop()
