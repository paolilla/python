from tkinter import *
import pandas
import random

# ---------------------------- CONSTANTS ------------------------------- #
BACKGROUND_COLOR = "#B1DDC6"
BLACK = "#000"
WHITE = "#FFF"

# --------------------- FLASHCARD FUNCTIONALITY ------------------------ #
try:
    data = pandas.read_csv("data/words_to_learn.csv") # Use custom file
except FileNotFoundError:
    original_data = pandas.read_csv("data/french_words.csv") # Use original file
    to_learn = original_data.to_dict(orient="records") # Create dictionary of words from original file
else:    
    to_learn = data.to_dict(orient="records") # Create dictionary of words from custom file

def next_card():
    global current_card 
    global flip_timer
    window.after_cancel(flip_timer) # Cancel previous timer
    current_card = random.choice(to_learn) # Choose random word from dictionary
    canvas.itemconfig(card_title, text="French", fill=BLACK) # Set language label to French
    canvas.itemconfig(card_word, text=current_card["French"], fill=BLACK) # Set word label to word in French
    canvas.itemconfig(card_image, image=card_front_image) # Set card image
    flip_timer = window.after(3000, func=flip_card) # Start timer to flip

def flip_card():
    canvas.itemconfig(card_title, text="English", fill=WHITE) # Set language label to English
    canvas.itemconfig(card_word, text=current_card["English"], fill=WHITE) # Set word label to English
    canvas.itemconfig(card_image, image=card_back_image) # Set word label to word in English

def is_known():
    to_learn.remove(current_card) # Remove current card from dictionary
    data = pandas.DataFrame(to_learn) # Convert dictionary to DataFrame
    data.to_csv("data/words_to_learn.csv", index=False) # Save DataFrame to .csv file
    next_card() # Go to next card

# ---------------------------- UI SETUP ------------------------------- #
window = Tk() # Create window
window.title("Flashy") # Set window title
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR) # Set window configurations
flip_timer = window.after(3000, func=flip_card) # Start first timer

# Canvas
canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0) # Create canvas and add configuration

# PhotoImages
card_front_image = PhotoImage(file="images/card_front.png")
card_back_image = PhotoImage(file="images/card_back.png")
wrong_image = PhotoImage(file="images/wrong.png")
right_image = PhotoImage(file="images/right.png")

card_image = canvas.create_image(400, 263, image=card_front_image) # Add image to canvas
card_title = canvas.create_text(400, 150, text="", font=("Arial", 40, "italic")) # Add language label to canvas
card_word = canvas.create_text(400, 263, text="", font=("Arial", 60, "bold")) # Add word label to canvas
canvas.grid(column=0, row=0, columnspan=2) # Add canvas to grid

#Button wrong
button_wrong = Button(image=wrong_image, highlightthickness=0, command=next_card) # Create button and add configuration
button_wrong.grid(column=0, row=1) # Add button to grid

#Button right
button_right = Button(image=right_image, highlightthickness=0, command=is_known) # Create button and add configuration
button_right.grid(column=1, row=1) # Add button to grid

next_card() # Go to first card

window.mainloop()