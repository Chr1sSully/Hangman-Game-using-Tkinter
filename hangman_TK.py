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


secret_word = ""
guessed_letters = []
wrong_guesses = []


# Initialise window
window = tk.Tk()
window.title("Hangman")


# Key bindings for keyboard
def on_return_key(event):
    take_guess()


def on_escape_key(event):
    start_game()


def get_word():
    with open('words.txt') as f:
        word_string = f.read()
        WORDLIST = word_string.split(' ')
        return random.choice(WORDLIST)


def start_game():
    global secret_word, guessed_letters, wrong_guesses
    secret_word = get_word()
    # print(secret_word)
    # print(guessed_letters)
    # print(wrong_guesses)
    guessed_letters = []
    wrong_guesses = []

    update_display()
    update_guess()
    letter_guess.focus()


def update_display():
    try:
        t1.delete('1.0', tk.END)
        t1.insert('1.0', HANGMAN_PICS[len(wrong_guesses)], "center")
    except:
        t1.delete('1.0', tk.END)
        t1.insert('1.0', "\n\nYou lost the game... :(\n", "center")
        t1.insert('1.0', "The word was... \n\n" + secret_word, "center")


def update_guess():
    # Update word to guess
    word_to_guess.delete(0, tk.END)
    for letter in secret_word:
        if letter not in guessed_letters:
            word_to_guess.insert('end', '_' + ' ')
        else:
            word_to_guess.insert('end', letter + ' ')

    if word_to_guess.get().replace(' ', '') == secret_word:
        t1.delete('1.0', tk.END)
        t1.insert(tk.END, "\n\nYou WON the game... :)\n", "center")
        t1.insert(tk.END, "The word was... \n\n" + secret_word, "center")
    # update previous guessed letters
    prev_guesses.delete(0, tk.END)
    for letter in guessed_letters:
        prev_guesses.insert(tk.END, letter + ' ')


def take_guess():
    the_guess = letter_guess.get()
    if the_guess in guessed_letters or len(the_guess) != 1 or secret_word == '':
        letter_guess.delete(0, tk.END)
        return None
    if the_guess in secret_word:
        guessed_letters.append(the_guess)
    else:
        guessed_letters.append(the_guess)
        wrong_guesses.append(the_guess)

    letter_guess.delete(0, tk.END)
    update_display()
    update_guess()



# Tkinter window setup
labelText = tk.StringVar()
labelText.set("Welcome to Hangman!")
labelDir = tk.Label(window, textvariable=labelText)
labelDir.pack()

t1 = tk.Text(window, height=10, width=40, font="Helvetica 18 bold")
t1.tag_configure("center", justify='center')
t1.tag_add("center", 1.0, "end")
t1.pack()
msg = '''\nWelcome to Hangman
Press Esc or press 
start game to begin
Once the game begins
Enter your letters below 
'''
t1.insert('1.0', msg, "center")

b_start = ttk.Button(window, text="Start Game", command=start_game)
b_start.pack()

labelText = tk.StringVar()
labelText.set("Word to guess")
labelDir = tk.Label(window, textvariable=labelText)
labelDir.pack()

word_to_guess = tk.Entry(window, font="Helvetica 44 bold", justify='center')
word_to_guess.pack()

labelText = tk.StringVar()
labelText.set("Enter 1 letter below to guess")
labelDir = tk.Label(window, textvariable=labelText)
labelDir.pack()

letter_guess = tk.Entry(window, font="Helvetica 44 bold", justify='center', width=2)
letter_guess.pack()
letter_guess.focus()

b_take_guess = ttk.Button(window, text="Have a guess", command=take_guess)
b_take_guess.pack()

labelText = tk.StringVar()
labelText.set("Your previous guesses")
labelDir = tk.Label(window, textvariable=labelText)
labelDir.pack()
prev_guesses = tk.Entry(window, font="Helvetica 24 bold", justify='center')
prev_guesses.pack()

window.bind('<Return>', on_return_key)
window.bind('<Escape>', on_escape_key)

# window.after(3000, start_game)
window.mainloop()
