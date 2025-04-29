import random
import tkinter as tk
import requests

# Уровни сложности
difficulty_levels = {
    'Easy': {'attempts': 10, 'difficulty': 'easy'},
    'Medium': {'attempts': 7, 'difficulty': 'medium'},
    'Hard': {'attempts': 5, 'difficulty': 'hard'}
}

def get_random_word(difficulty):
    difficulty_mapping = {
        'easy': random.randint(4, 6),  # Easy: 4-6 letters
        'medium': random.randint(7, 9),  # Medium: 7-9 letters
        'hard': random.randint(10, 12)  # Hard: 10-12 letters
    }
    word_length = difficulty_mapping.get(difficulty, 5)
    url = f"https://random-word-api.herokuapp.com/word?number=1&length={word_length}"

    try:
        response = requests.get(url)
        if response.status_code != 200:
            print(f"Request error: {response.status_code}")
            return "default"

        try:
            data = response.json()
            if not data or not isinstance(data, list):
                print("Error: received invalid JSON.")
                return "default"
            return data[0]
        except ValueError as e:
            print("JSON processing error:", e)
            return "default"
    except requests.exceptions.RequestException as e:
        print("Connection error:", e)
        return "default"

# Initialization of statistics
stats = {"games_played": 0, "games_won": 0, "games_lost": 0}

class HangmanApp:
    def __init__(self, master):
        self.master = master
        self.master.title("The Hangman Game")
        self.master.geometry("500x500")
        self.difficulty = None

        # Start screen
        self.start_screen()

    def start_screen(self):
        # Cleaning the window
        for widget in self.master.winfo_children():
            widget.destroy()

        # Reset statistics before starting a new game
        stats["games_played"] = 0
        stats["games_won"] = 0
        stats["games_lost"] = 0

        title = tk.Label(self.master, text="Welcome to the Hangman!", font=("Arial", 24))
        title.pack(pady=20)

        instruction = tk.Label(self.master, text="Choose the level of difficulty:", font=("Arial", 20))
        instruction.pack(pady=10)

        # Difficulty level buttons
        for level, config in difficulty_levels.items():
            button = tk.Button(self.master, text=level, font=("Arial", 16),
                               command=lambda lvl=config['difficulty']: self.start_game(lvl))
            button.pack(pady=5)

    def start_game(self, difficulty):
        self.difficulty = difficulty
        # Cleaning the window
        for widget in self.master.winfo_children():
            widget.destroy()

        # Start the game
        self.game = HangmanGame(self.master, self.difficulty, self.start_screen)

class HangmanGame:
    def __init__(self, master, difficulty, back_callback):
        self.master = master
        self.difficulty = difficulty
        self.back_callback = back_callback

        self.attempts = 0
        self.word = ""
        self.guessed_word = []
        self.guessed_letters = []
        self.incorrect_guesses = 0
        self.game_over = False

        # Game interface
        self.create_game_ui()

        # Starting a new game
        self.start_new_game()

    def create_game_ui(self):
        """Creates interface elements for the game."""
        # Back button
        self.back_button = tk.Button(self.master, text="Back", command=self.back_callback)
        self.back_button.pack(pady=5)

        # Tries
        self.attempts_label = tk.Label(self.master, text="Tries: 0", font=("Arial", 12))
        self.attempts_label.pack(pady=5)

        # Guessed word
        self.word_label = tk.Label(self.master, text="Guessed word: ", font=("Arial", 14))
        self.word_label.pack(pady=10)

        # Message to user
        self.message_label = tk.Label(self.master, text="", font=("Arial", 12))
        self.message_label.pack(pady=5)

        # Field for entering a letter
        self.input_label = tk.Label(self.master, text="Enter letter:", font=("Arial", 12))
        self.input_label.pack(pady=5)

        self.entry = tk.Entry(self.master, font=("Arial", 14))
        self.entry.pack(pady=5)

        self.submit_button = tk.Button(self.master, text="Submit", command=self.check_guess)
        self.submit_button.pack(pady=5)

        # Statistics
        self.stats_label = tk.Label(self.master, text=f"Wins: {stats['games_won']} | Losses: {stats['games_lost']}", font=("Arial", 12))
        self.stats_label.pack(pady=10)

        # New Game button
        self.new_game_button = tk.Button(self.master, text="New Game", command=self.start_new_game)
        self.new_game_button.pack(pady=10)
        self.new_game_button.pack_forget()

        # Canvas for painting the hangman
        self.canvas = tk.Canvas(self.master, width=200, height=200)
        self.canvas.pack(pady=10)

        # Label for wrong letters
        self.incorrect_guesses_label = tk.Label(self.master, text="Wrong letters: ", font=("Arial", 12))
        self.incorrect_guesses_label.pack(pady=5)

        # Bind the Enter key to input a letter
        self.master.bind("<Return>", self.on_enter_press)

    def on_enter_press(self, event):
        """Treats pressing the Enter key as a confirmation of letter input."""
        self.check_guess()

    def draw_gallows(self):
        """Draws the hangman step by step depending on the number of wrong letters."""
        self.canvas.delete("all")  # Clean the canvas before painting

        # Drawing the hangman depending on the difficulty
        if self.difficulty == "easy" or self.difficulty == "medium":
            if self.incorrect_guesses >= 1:
                self.canvas.create_line(50, 150, 150, 150)  # Base
            if self.incorrect_guesses >= 2:
                self.canvas.create_line(100, 150, 100, 50)  # Pillar
            if self.incorrect_guesses >= 3:
                self.canvas.create_line(100, 50, 150, 50)  # The bar
            if self.incorrect_guesses >= 4:
                self.canvas.create_line(150, 50, 150, 80)  # Vertical line

        if self.difficulty == "hard":
            if self.incorrect_guesses >= 1:
                self.canvas.create_line(50, 150, 150, 150)  # Base
                self.canvas.create_line(100, 150, 100, 50)  # Pillar
            if self.incorrect_guesses >= 2:
                self.canvas.create_line(100, 50, 150, 50)  # The bar
                self.canvas.create_line(150, 50, 150, 80)  # Vertical line
            if self.incorrect_guesses >= 3:
                self.canvas.create_oval(140, 80, 160, 100)  # Head
                self.canvas.create_line(150, 100, 150, 120)  # Body
            if self.incorrect_guesses >= 4:
                self.canvas.create_line(150, 120, 130, 140)  # Left foot
                self.canvas.create_line(150, 120, 170, 140)  # Right foot
            if self.incorrect_guesses >= 5:
                self.canvas.create_line(150, 110, 130, 100)  # Левая рука
                self.canvas.create_line(150, 110, 170, 100)  # Правая рука

        elif self.difficulty == "medium":
            if self.incorrect_guesses >= 5:
                self.canvas.create_oval(140, 80, 160, 100)  # Head
                self.canvas.create_line(150, 100, 150, 120)  # Body
            if self.incorrect_guesses >= 6:
                self.canvas.create_line(150, 120, 130, 140)  # Left foot
                self.canvas.create_line(150, 120, 170, 140)  # Right foot
            if self.incorrect_guesses >= 7:
                self.canvas.create_line(150, 110, 130, 100)  # Left hand
                self.canvas.create_line(150, 110, 170, 100)  # Right hand

        else:
            if self.incorrect_guesses >= 5:
                self.canvas.create_oval(140, 80, 160, 100)  # Head
            if self.incorrect_guesses >= 6:
                self.canvas.create_line(150, 100, 150, 120) # Body
            if self.incorrect_guesses >= 7:
                self.canvas.create_line(150, 120, 130, 140)  # Left foot
            if self.incorrect_guesses >= 8:
                self.canvas.create_line(150, 120, 170, 140)  # Right foot
            if self.incorrect_guesses >= 9:
                self.canvas.create_line(150, 110, 130, 100)  # Left hand
            if self.incorrect_guesses >= 10:
                self.canvas.create_line(150, 110, 170, 100)  # Right hand

    def start_new_game(self):
        self.word = get_random_word(self.difficulty)
        self.guessed_word = ["_"] * len(self.word)
        self.guessed_letters = []
        self.incorrect_guesses = 0
        self.game_over = False
        self.attempts = difficulty_levels['Easy']['attempts'] if self.difficulty == 'easy' else (
            difficulty_levels['Medium']['attempts'] if self.difficulty == 'medium' else difficulty_levels['Hard']['attempts']
        )
        self.message_label.config(text="")
        self.new_game_button.pack_forget()
        self.entry.config(state=tk.NORMAL)
        self.submit_button.config(state=tk.NORMAL)
        self.update_ui()

    def check_guess(self):
        if self.game_over:
            return

        letter = self.entry.get().lower()
        self.entry.delete(0, tk.END)

        if len(letter) != 1 or not letter.isalpha():
            self.message_label.config(text="Enter one letter!")
            return

        if letter in self.guessed_letters:
            self.message_label.config(text="You've already tried this letter!")
            return

        self.guessed_letters.append(letter)

        if letter in self.word:
            for i, char in enumerate(self.word):
                if char == letter:
                    self.guessed_word[i] = letter
            self.message_label.config(text="Correct letter!")
        else:
            self.incorrect_guesses += 1
            self.attempts -= 1
            self.message_label.config(text=f"Wrong! Tries left: {self.attempts}")

        if "_" not in self.guessed_word:
            stats['games_won'] += 1
            self.end_game(win=True)
        elif self.attempts <= 0:
            stats['games_lost'] += 1
            self.end_game(win=False)

        self.update_ui()

    def end_game(self, win):
        self.game_over = True
        if win:
            self.message_label.config(text=f"Congratulations! You guessed the word: {self.word}")
        else:
            self.message_label.config(text=f"You lost! The word was: {self.word}")
        self.entry.config(state=tk.DISABLED)
        self.submit_button.config(state=tk.DISABLED)
        self.new_game_button.pack()

    def update_ui(self):
        self.word_label.config(text=f"Guessed word: {' '.join(self.guessed_word)}")
        self.attempts_label.config(text=f"Tries: {self.attempts}")
        self.stats_label.config(text=f"Wins: {stats['games_won']} | Losses: {stats['games_lost']}")
        self.incorrect_guesses_label.config(text=f"Wrong letters: {', '.join([letter for letter in self.guessed_letters if letter not in self.word])}")
        self.draw_gallows()

        
# Run the app
root = tk.Tk()
app = HangmanApp(root)
root.mainloop()

