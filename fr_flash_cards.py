#   fr_flash_cards
# Tests the user on common french words

from tkinter import *
import pandas
import random

BACKGROUND_COLOR = "#B1DDC6"

current_card = {}
to_learn = {}

try:
    data = pandas.read_csv("words_to_learn.csv")
except FileNotFoundError:
    original_data = pandas.read_csv("french_words.csv")
    to_learn = original_data.to_dict(orient='records')
else:
    to_learn = data.to_dict(orient='records')


# --------------------------- Front Words ----------------------------- #
def next_french_word():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(to_learn)
    canvas.itemconfig(title_card, text="French", fill="black")
    canvas.itemconfig(word_card, text=current_card["French"], fill="black")
    canvas.itemconfig(card_background, image=card_front_img)
    flip_timer = window.after(3000, func=eng_back_card)


# --------------------------- Front Words ----------------------------- #
def eng_back_card():
    # global current_card
    canvas.itemconfig(title_card, text="English", fill="white")
    canvas.itemconfig(word_card, text=current_card["English"], fill="white")
    canvas.itemconfig(card_background, image=card_back_img)


def is_known():
    to_learn.remove(current_card)
    data_file = pandas.DataFrame(to_learn)
    data_file.to_csv("words_to_learn.csv", index=False)
    next_french_word()


# --------------------------- Create UI ----------------------------- #
window = Tk()
window.title("Flashy")

window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

flip_timer = window.after(3000, func=eng_back_card)


# Create Card Canvas
canvas = Canvas(width=800, height=526)
card_front_img = PhotoImage(file="card_front.png")
card_back_img = PhotoImage(file="card_back.png")
card_background = canvas.create_image(400, 263, image=card_front_img)
canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
title_card = canvas.create_text(400, 150, text="", font=("Arial", 35, "italic"))
word_card = canvas.create_text(400, 263, text="", font=("Arial", 55, "bold"))
canvas.grid(column=0, row=0, columnspan=2)

# Create and place wrong and right Buttons
wrong_image = PhotoImage(file="wrong.png")
wrong_button = Button(image=wrong_image, highlightthickness=0, command=next_french_word)
wrong_button.grid(column=0, row=1)
right_image = PhotoImage(file="right.png")
right_button = Button(image=right_image, highlightthickness=0, command=is_known)
right_button.grid(column=1, row=1)


next_french_word()
window.mainloop()
