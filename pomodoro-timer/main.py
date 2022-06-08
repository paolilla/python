from tkinter import *
import math

# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20
reps = 0
timer = None

# ---------------------------- TIMER RESET ------------------------------- # 
def reset_timer():
    window.after_cancel(timer) # Cancel execution of timer
    canvas.itemconfig(timer_text, text="00:00") # Reset canvas
    title_label.config(text="Timer", fg=GREEN) # Reset label
    check_marks.config(text="") # Reset checkmarks
    global reps 
    reps = 0 # Reset reps

# ---------------------------- TIMER MECHANISM ------------------------------- # 
def start_timer():
    global reps # Get global variable reps
    reps += 1 # Increase reps by one
    work_sec = WORK_MIN * 60
    short_break_sec = SHORT_BREAK_MIN * 60
    long_break_sec = LONG_BREAK_MIN * 60

    if reps % 8 == 0:
        count_down(long_break_sec) # Call long break
        title_label.config(text="Break", fg=RED) # Change label text and color
    elif reps % 2 == 0:
        count_down(short_break_sec) # Call short break
        title_label.config(text="Break", fg=PINK) # Change label text and color
    else: 
        count_down(work_sec) # Call work time
        title_label.config(text="Work", fg=GREEN) # Change label text and color

# ---------------------------- COUNTDOWN MECHANISM ------------------------------- # 
def count_down(count):
    count_min = math.floor(count/60) # Calculate minutes left
    count_sec = count % 60 # Calculate seconds left

    if count_sec < 10: 
        count_sec = f"0{count_sec}" # Format for clock 

    canvas.itemconfig(timer_text, text=f"{count_min}:{count_sec}") # Change label to show time

    if count > 0: 
        global timer
        timer = window.after(1000, count_down, count - 1) # Wait a second a run again
    else:
        start_timer() 
        marks = "" 
        work_sessions = math.floor(reps/2) # Get work sessions
        for _ in range(work_sessions):
            marks += "✓" # Add marks text
        check_marks.config(text=marks) # Add marks to label

# ---------------------------- UI SETUP ------------------------------- #
window = Tk() # Creating windows
window.title("Pomodoro!") # Adding title to window
window.config(padx=100, pady=50, bg=YELLOW) # Configuring window

# Creating Timer label
title_label = Label(text="Timer", fg=GREEN, bg=YELLOW, font=(FONT_NAME, 40, "bold")) # Configuring label
title_label.grid(column=1, row=0) # Adding label to grid

# Creating Canvas
canvas = Canvas(width=200, height=224, bg=YELLOW, highlightthickness=0) # Configuring canvas
tomato_img = PhotoImage(file="tomato.png") # Creating image object
canvas.create_image(100, 112, image=tomato_img) # Adding image to canvas
timer_text = canvas.create_text(100, 130, text="00:00", fill="white", font=(FONT_NAME, 35, "bold")) # Adding text to canvas
canvas.grid(column=1, row=1) # Adding canvas to grid

# Creating buttons
start_button = Button(text="Start", font=(FONT_NAME, 10, "bold"), highlightthickness=0, command=start_timer) # Creating start button
reset_button = Button(text="Reset", font=(FONT_NAME, 10, "bold"), highlightthickness=0, command=reset_timer) # Creating reset button
start_button.grid(column=0, row=2) # Adding start button to grid
reset_button.grid(column=2, row=2) # Adding reset button to grid

# Creating check marks
check_marks = Label(text="", bg=YELLOW, fg=GREEN, font=(FONT_NAME, 15)) # Creating check marks
check_marks.grid(column=1, row=3) # Adding check marks to grid

window.mainloop() # Running window