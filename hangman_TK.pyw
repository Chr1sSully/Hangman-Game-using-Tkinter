import random
import tkinter as tk
from tkinter import ttk


HANGMAN_PICS = ['''
 +---+
     |
     |
     |
    ===''', '''
 +---+
 O   |
     |
     |
    ===''', '''
 +---+
 O   |
 |   |
     |
    ===''', '''
 +---+
 O   |
/|   |
     |
    ===''', '''
 +---+
 O   |
/|\  |
     |
    ===''', '''
 +---+
 O   |
/|\  |
/    |
    ===''', '''
 +---+
 O   |
/|\  |
/ \  |
    ===''', '''
 +---+
[O   |
/|\  |
/ \  |
    ===''', '''
 +---+
[O]  |
/|\  |
/ \  |
    ===''']


class MyGui:
    def __init__(self, master):
        self.master = master
        master.title = 'Hangman'

        # Setup widgets
        self.labelText = tk.StringVar()
        self.labelText.set("Welcome to Hangman!")
        self.labelDir = ttk.Label(master, textvariable=self.labelText)
        self.labelDir.pack()

        self.main_text = tk.Text(master, height=10, width=40, font="Helvetica 18 bold")
        self.main_text.tag_configure("center", justify='center')
        self.main_text.tag_add("center", 1.0, "end")
        self.main_text.pack()
        msg = '''\nWelcome to Hangman
        Press Esc or press 
        start game to begin
        Once the game begins
        Enter your letters below 
        '''
        self.main_text.insert('1.0', msg, "center")

        self.b_start = ttk.Button(master, text="Start Game", command=self.start_game)
        self.b_start.pack()

        self.labelText = tk.StringVar()
        self.labelText.set("Word to guess")
        self.labelDir = ttk.Label(master, textvariable=self.labelText)
        self.labelDir.pack()

        self.word_to_guess = ttk.Entry(master, font="Helvetica 44 bold", justify='center')
        self.word_to_guess.pack()

        self.labelText = tk.StringVar()
        self.labelText.set("Enter 1 letter below to guess")
        self.labelDir = ttk.Label(master, textvariable=self.labelText)
        self.labelDir.pack()

        self.letter_guess = ttk.Entry(master, font="Helvetica 44 bold", justify='center', width=2)
        self.letter_guess.pack()
        self.letter_guess.focus()

        self.b_take_guess = ttk.Button(master, text="Have a guess", command=self.take_guess)
        self.b_take_guess.pack()

        self.labelText = tk.StringVar()
        self.labelText.set("Your previous guesses")
        self.labelDir = ttk.Label(master, textvariable=self.labelText)
        self.labelDir.pack()
        self.prev_guesses = ttk.Entry(master, font="Helvetica 24 bold", justify='center')
        self.prev_guesses.pack()

    @staticmethod
    def get_word():
        with open('words.txt') as f:
            word_string = f.read()
            WORDLIST = word_string.split(' ')
            return random.choice(WORDLIST)

    def on_return_key(self, event):
        self.take_guess()

    def on_escape_key(self, event):
        self.start_game()

    def start_game(self):
        self.secret_word = self.get_word()
        self.guessed_letters = []
        self.wrong_guesses = []
        self.update_display()
        self.update_guess()
        self.letter_guess.focus()

    def update_display(self):
        try:
            self.main_text.delete('1.0', tk.END)
            self.main_text.insert('1.0', HANGMAN_PICS[len(self.wrong_guesses)], "center")
        except:
            self.main_text.delete('1.0', tk.END)
            self.main_text.insert('1.0', "\n\nYou lost the game... :(\n", "center")
            self.main_text.insert('1.0', "The word was... \n\n" + self.secret_word, "center")

    def update_guess(self):
        # Update word to guess
        self.word_to_guess.delete(0, tk.END)
        for letter in self.secret_word:
            if letter not in self.guessed_letters:
                self.word_to_guess.insert('end', '_' + ' ')
            else:
                self.word_to_guess.insert('end', letter + ' ')

        if self.word_to_guess.get().replace(' ', '') == self.secret_word:
            self.main_text.delete('1.0', tk.END)
            self.main_text.insert(tk.END, "\n\nYou WON the game... :)\n", "center")
            self.main_text.insert(tk.END, "The word was... \n\n" + self.secret_word, "center")
        # update previous guessed letters
        self.prev_guesses.delete(0, tk.END)
        for letter in self.wrong_guesses:
            self.prev_guesses.insert(tk.END, letter + ' ')

    def take_guess(self):
        the_guess = self.letter_guess.get().lower()
        if the_guess in self.guessed_letters or len(the_guess) != 1 or self.secret_word == '':
            self.letter_guess.delete(0, tk.END)
            return None
        if the_guess in self.secret_word:
            self.guessed_letters.append(the_guess)
        else:
            self.guessed_letters.append(the_guess)
            self.wrong_guesses.append(the_guess)

        self.letter_guess.delete(0, tk.END)
        self.update_display()
        self.update_guess()


root = tk.Tk()
my_gui = MyGui(root)

root.bind('<Return>', my_gui.on_return_key)
root.bind('<Escape>', my_gui.on_escape_key)

# window.after(3000, start_gamemy_gui.)
root.mainloop()
