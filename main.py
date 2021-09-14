from tkinter import *
from tkinter import messagebox
import random
import pyperclip
import json


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate():
    password_entry.delete(0, END)
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v',
               'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q',
               'R',
               'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '*', '+']

    pass_letters = [random.choice(letters) for _ in range(random.randint(6, 8))]
    pass_symbols = [random.choice(symbols) for _ in range(random.randint(1, 2))]
    pass_numbers = [random.choice(numbers) for _ in range(random.randint(2, 3))]
    password_list = pass_numbers + pass_symbols + pass_letters
    random.shuffle(password_list)
    generated_pass = "".join(password_list)
    password_entry.insert(0, generated_pass)
    pyperclip.copy(generated_pass)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def get_data():
    website = website_entry.get().title()
    username = username_entry.get()
    password = password_entry.get()

    if website == "" or username == "" or password == "":
        messagebox.showerror(title="oops", message="Please don't leave any fields empty")
    else:
        cred = {
            website: {
                "email": username,
                "password": password
            }
        }
        try:
            with open("data.json", "r") as data_file:
                data = json.load(data_file)
                data.update(cred)
        except (json.decoder.JSONDecodeError, FileNotFoundError):
            with open("data.json", "w") as data_file:
                json.dump(cred, data_file, indent=4)
        else:
            with open("data.json", "w") as data_file:
                json.dump(data, data_file, indent=4)
        finally:
            website_entry.delete(0, END)
            password_entry.delete(0, END)


# ---------------------------- SEARCH PASSWORD ------------------------------- #
def find_password():
    website = website_entry.get().title()
    if website != "":
        try:
            with open("data.json", "r") as data_file:
                data = json.load(data_file)
                email = data[website]['email']
                password = data[website]['password']
                message = f"Email: {email}\nPassword: {password}\n\nPassword copied to clipboard"
                messagebox.showinfo(title=website, message=message)
                pyperclip.copy(password)
        except (KeyError, FileNotFoundError):
            messagebox.showerror(title="oops", message="You don't have a password for this website")


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.minsize(width=200, height=200)
window.config(padx=50, pady=50)

canvas = Canvas(width=210, height=200, highlightthickness=0)
logo_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_img)
canvas.grid(column=2, row=1)

# Labels
website_label = Label(text="Website:")
website_label.grid(column=1, row=2)

username_label = Label(text="Email/Username:")
username_label.grid(column=1, row=3)

password_label = Label(text="Password:")
password_label.grid(column=1, row=4)

# Entries
website_entry = Entry(width=21)
website_entry.grid(column=2, row=2, columnspan=1, sticky=EW)
website_entry.focus()

username_entry = Entry(width=35)
username_entry.grid(column=2, row=3, columnspan=2, sticky=EW)
username_entry.insert(END, 'elonsh2@gmail.com')

password_entry = Entry(width=21)
password_entry.grid(column=2, row=4, sticky=EW)

# Buttons
generate_pass_button = Button(text="Generate Password", command=generate)
generate_pass_button.grid(column=3, row=4)

add_button = Button(text="Add", command=get_data, width=36)
add_button.grid(column=2, row=5, columnspan=2, sticky=EW)

search_button = Button(text="Search", command=find_password)
search_button.grid(column=3, row=2, columnspan=1, sticky=EW)


window.mainloop()
