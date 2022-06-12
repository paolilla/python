from tkinter import *
from tkinter import messagebox
from random import choice, randint, shuffle
import json
import pyperclip

# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'] # List of letters
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'] # List of numbers
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+'] # List of symbols

    password_letters = [choice(letters) for _ in range(randint(8, 10))] # Create a randomized list containing from 8 to 10 letters
    password_symbols = [choice(symbols) for _ in range(randint(2, 4))] # Create a randomized list containing from 2 to 4 symbols
    password_numbers = [choice(numbers) for _ in range(randint(2, 4))] # Create a randomized list containing from 2 to 4 numbers

    password_list = password_letters + password_symbols + password_numbers # Join all password lists
    shuffle(password_list) # Shuffle contents of password list

    password = "".join(password_list) # Join all items of password list into one string
    password_entry.insert(0, password) # Insert password into password_entry
    pyperclip.copy(password) # Copy password to clipboard

# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():

    website = website_entry.get() # Get website from entry
    email = email_entry.get() # Get email from entry
    password = password_entry.get() # Get password from entry
    # Create dictionary for JSON file
    new_data = {website: {
        "email": email,
        "password": password,
    }}

    if len(website) == 0 or len(password) == 0: # If website or password entries are empty
        messagebox.showinfo(title="Oops", message="Please make sure you haven't left any fields empty.") # Show warning message
    else:
        try:
            with open("data.json", "r") as data_file: # Open text data file
                data = json.load(data_file) # Read old data
        except FileNotFoundError:
            with open("data.json", "w") as data_file:
                json.dump(new_data, data_file, indent=4) # Saving updated data
        else:
            data.update(new_data) # Update old data with new data

            with open("data.json", "w") as data_file:
                json.dump(data, data_file, indent=4) # Saving updated data
        finally:
            website_entry.delete(0, END) # Clean website entry
            password_entry.delete(0, END) # Clean password entry

# ---------------------------- FIND PASSWORD ------------------------------- #
def find_password():
    
    website = website_entry.get() # Get website from entry
    try: 
        with open("data.json") as data_file: # Open JSON file
            data = json.load(data_file) # Load data from JSON file
    except FileNotFoundError: # Handle error 
        messagebox.showinfo(title="Error", message="No Data File Found") # Show FileNotFoundError message
    else:
        if website in data: # If website has been found within data
            email = data[website]["email"] # Get email
            password = data[website]["password"] # Get password
            messagebox.showinfo(title=website, message=f"Email: {email}\nPassword: {password}") # Show email and password found for website
        else:
            messagebox.showinfo(title="Error", message=f"No details for {website} exist.") # Show message that no details have been found

# ---------------------------- UI SETUP ------------------------------- #
window = Tk() # Create window
window.title("Password Manager") # Add title to window
window.config(padx=20, pady=20) # Add padding to window

canvas = Canvas(width=200, height=200) # Create canvas and add custom size
logo_img = PhotoImage(file="lock.png") # Create image object
canvas.create_image(100, 100, image=logo_img) # Add image to canvas
canvas.grid(row=0, column=1) # Add canvas to grid

# Labels
website_label = Label(text="Website:") # Website label
website_label.grid(row=1, column=0) # Add label to grid

email_label = Label(text="Email/Username:") # Email label
email_label.grid(row=2, column=0) # Add label to grid

password_label = Label(text="Password:") # Password label
password_label.grid(row=3, column=0) # Add label to grid

# Buttons
generate_password_button = Button(text="Generate Password", command=generate_password) # Generate Password button
generate_password_button.grid(row=3, column=2) # Add button to grid

add_button = Button(text="Add", width=36, command=save) # Add password button
add_button.grid(row=4, column=1, columnspan=2) # Add button to grid

search_button = Button(text="Search", width=13, command=find_password) # Generate Password button
search_button.grid(row=1, column=2) # Add button to grid

# Entries
website_entry = Entry(width=21) # Website entry
website_entry.grid(row=1, column=1) # Add entry to grid
website_entry.focus() # Automatically focus on entry

email_entry = Entry(width=35) # Email entry
email_entry.grid(row=2, column=1, columnspan=2) # Add entry to grid
email_entry.insert(0, "email@email.com") # Fill entry by default

password_entry = Entry(width=21) # Password entry
password_entry.grid(row=3, column=1) # Add entry to grid

window.mainloop() 