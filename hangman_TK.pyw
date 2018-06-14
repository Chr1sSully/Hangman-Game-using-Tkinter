import random
import tkinter as tk
from tkinter import ttk
from hangman_pics import HANGMAN_PICS
import sys
'''
Simple hangman game using Tkinter, requires .txt file with word list in same directory
'''


class MyGui:
    def __init__(self, master):
        self.master = master
        self.secret_word = ''
        self.running = False
        self.start_msg = '''\n
        Welcome to Hangman
        Press Enter or click 
        start game to begin
        Once the game begins
        Enter your letters below 
        '''

        self.make_widgets()
        self.reset_guesses()

    def reset_guesses(self):
        self.guessed_letters = []
        self.wrong_guesses = []

    def make_widgets(self):
        ''' Setup all the widgets '''
        # Top label
        self.headerText = tk.StringVar()
        self.headerText.set('Welcome to Hangman!')
        self.labelDir = tk.Label(self.master, textvariable=self.headerText)
        self.labelDir.pack()
        # Top text box
        self.main_text = tk.Text(self.master, height=10, width=40, font='Helvetica 18 bold')
        self.main_text.tag_configure('center', justify='center')
        self.main_text.tag_add('center', 1.0, 'end')
        self.main_text.pack()
        self.main_text.insert('1.0', self.start_msg, 'center')
        # Start button
        self.b_start = ttk.Button(self.master, text='Start Game', command=self.start_game)
        self.b_start.pack()
        # Label + box for the unkown word
        self.labelText = tk.StringVar()
        self.labelText.set('Word to guess')
        self.labelDir = tk.Label(self.master, textvariable=self.labelText)
        self.labelDir.pack()
        self.word_to_guess = ttk.Entry(self.master, font='Helvetica 44 bold', justify='center')
        self.word_to_guess.pack()
        # Label + box for guess entry box
        self.labelText = tk.StringVar()
        self.labelText.set('Enter 1 letter below to guess')
        self.labelDir = tk.Label(self.master, textvariable=self.labelText)
        self.labelDir.pack()
        self.letter_guess = ttk.Entry(self.master, font='Helvetica 44 bold', justify='center', width=2)
        self.letter_guess.pack()
        self.letter_guess.focus()
        # Button to take guess
        self.b_take_guess = ttk.Button(self.master, text='Have a guess', command=self.take_guess)
        self.b_take_guess.pack()
        # Label + box for the wrong guesses
        self.labelText = tk.StringVar()
        self.labelText.set('Your previous guesses')
        self.labelDir = tk.Label(self.master, textvariable=self.labelText)
        self.labelDir.pack()
        self.prev_guesses = ttk.Entry(self.master, font='Helvetica 24 bold', justify='center')
        self.prev_guesses.pack()

    @staticmethod
    def get_word():
        with open('words.txt') as f:
            word_string = f.read()
            WORDLIST = word_string.split(' ')
            return random.choice(WORDLIST)

    @staticmethod
    def end_game():
        sys.exit()

    def on_return_key(self, event):
        # Either start the game or take a guess
        if self.running:
            self.take_guess()
        else:
            self.start_game()

    def on_escape_key(self, event):
        self.end_game()

    def start_game(self):
        ''' Initialise a new game '''
        self.running = True
        self.secret_word = self.get_word()
        # print(self.secret_word)
        self.reset_guesses()
        self.update_display()
        self.update_guess()
        self.letter_guess.focus()

    def update_display(self):
        ''' Update the main display to show how many guesses taken '''
        if len(self.wrong_guesses) <= len(HANGMAN_PICS) - 1:
            # Still have more guesses to go
            self.main_text.delete('1.0', tk.END)
            self.main_text.insert('1.0', HANGMAN_PICS[len(self.wrong_guesses)], 'center')
        else:
            # Out of guesses, game over
            self.main_text.delete('1.0', tk.END)
            loss_msg = f'\n\nYou LOST the game... :(\nThe word was...\n{self.secret_word}\nPress enter or click below to play again'
            self.main_text.insert(tk.END, loss_msg, 'center')
            self.running = False

    def update_guess(self):
        ''' Updates the word to guess box with guessed characters inserted 
            once they have been guessed '''
        if self.running:
            self.word_to_guess.delete(0, tk.END)
            for letter in self.secret_word:
                if letter not in self.guessed_letters:
                    self.word_to_guess.insert('end', '_' + ' ')
                else:
                    self.word_to_guess.insert('end', letter + ' ')

            if self.word_to_guess.get().replace(' ', '') == self.secret_word:
                self.main_text.delete('1.0', tk.END)
                win_msg = f'\n\nYou WON the game... :)\nThe word was...\n{self.secret_word}\nPress enter or click below to play again'
                self.main_text.insert(tk.END, win_msg, 'center')
                self.running = False
                return
            # update previous guessed letters box
            self.prev_guesses.delete(0, tk.END)
            for letter in self.wrong_guesses:
                self.prev_guesses.insert(tk.END, letter + ' ')

    def take_guess(self):
        ''' Takes a guess if the game is running, guess is only 1 letter 
            and the guess is a letter character '''
        if self.running:
            the_guess = self.letter_guess.get().lower()
            if the_guess in self.guessed_letters or len(the_guess) != 1 or not the_guess.isalpha():
                self.letter_guess.delete(0, tk.END)
                return
            if the_guess in self.secret_word:
                self.guessed_letters.append(the_guess)
            else:
                self.guessed_letters.append(the_guess)
                self.wrong_guesses.append(the_guess)

            self.letter_guess.delete(0, tk.END)
            self.update_display()
            self.update_guess()
        else:
            self.letter_guess.delete(0, tk.END)


root = tk.Tk()
root.title('Hangman')
my_gui = MyGui(root)


root.bind('<Return>', my_gui.on_return_key)
root.bind('<Escape>', my_gui.on_escape_key)

root.mainloop()
