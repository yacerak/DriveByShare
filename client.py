from customtkinter import *
from tools import *
import sqlite3
import PIL.Image, PIL.ImageTk
from io import BytesIO
from server import server

myfont=("Arial", 14)
white= "#FFFFFF"
app, frame = modern_window("Drive by Share")
app.geometry("850x500")



def submit_payment(pay_screen, id, hours, days):
    cursor.execute("SELECT * FROM cars WHERE id = ?", (id,))
    pph = cursor.fetchone()[3]

    price = (int(hours)*pph)+(int(days)*24*pph)
    timer = (int(hours)+int(days)*24)*3600
    cursor.execute("UPDATE cars SET time = ? WHERE id = ?", (timer, id))
    client = generate_secret_code()
    cursor.execute("UPDATE cars SET client = ? WHERE id = ?", (client, id))
    data = {
        "hours: ": hours,
        "days: ": days,
        "price: ": price,
        "client: ": client
    }
    Qrcode(data)
    cursor.execute("UPDATE cars SET availability = ? WHERE id = ?", (False, id))

    connection.commit()

    pay_screen.destroy()


def book(id):
    window = CTkToplevel(app)
    window.geometry("320x190")

    CTkLabel(window, text="hours").grid(row=0, column=0)
    hours_entry = CTkSpinbox(window, from_=0, to=24)
    hours_entry.grid(row=0, column=1)

    CTkLabel(window, text="days").grid(row=1, column=0)
    days_entry = CTkSpinbox(window, from_=0, to=60)
    days_entry.grid(row=1, column=1)

    CTkLabel(window, text="email:").grid(row=2, column=0)
    email_entry = CTkEntry(window)
    email_entry.grid(row=2, column=1)

    CTkLabel(window, text="Name on Card:").grid(row=3, column=0)
    name_entry = CTkEntry(window)
    name_entry.grid(row=3, column=1)

    CTkLabel(window, text="Card Number:").grid(row=4, column=0)
    card_number_entry = CTkEntry(window)
    card_number_entry.grid(row=4, column=1)

    CTkLabel(window, text="Expiration Date (YYYY/MM):").grid(row=5, column=0)
    expiration_entry = CTkEntry(window)
    expiration_entry.grid(row=5, column=1)

    CTkLabel(window, text="CVV/CVD:").grid(row=6, column=0)
    cvv_entry = CTkEntry(window)
    cvv_entry.grid(row=6, column=1)

    # Create a "Pay" button to submit the payment form
    pay_button = CTkButton(window, text="Pay", text_color=white,
                        command=lambda: submit_payment(window, id, hours_entry.get(), days_entry.get()))
    pay_button.grid(row=7, column=1)


def lessor():
    window = CTkToplevel(app)
    # Create a connection to the SQLite database
    conn = sqlite3.connect('accounts.db')
    c = conn.cursor()

    def save_acc(first, last, email, username, password, repassword, label):
        if (first.get() or last.get() or email.get() or username.get() or password.get() or repassword.get())==None:
            label.config(text="messing informations")

        elif password.get()!=repassword.get():
            label.config(text="incorrect password")
        else:
            # Insert the user's information into the accounts table
            c.execute("INSERT INTO accounts VALUES (?, ?, ?, ?, ?)", (first.get(), last.get(), email.get(), username.get(), password.get()))
            conn.commit()
            window.destroy()
            server()

    # Define a function to handle the sign up button
    def sign_up():
        for widget in window.winfo_children():
            widget.destroy()
        # Create the sign up fields
        CTkLabel(window, text="First Name:").grid(row=0, column=0)
        first_name_entry = CTkEntry(window)
        first_name_entry.grid(row=0, column=1)

        CTkLabel(window, text="Last Name:").grid(row=1, column=0)
        last_name_entry = CTkEntry(window)
        last_name_entry.grid(row=1, column=1)

        email_label = CTkLabel(window, text="Email:").grid(row=2, column=0)
        email_entry = CTkEntry(window)
        email_entry.grid(row=2, column=1)

        CTkLabel(window, text="Username:").grid(row=3, column=0)
        username_entry = CTkEntry(window)
        username_entry.grid(row=3, column=1)

        CTkLabel(window, text="Password:").grid(row=4, column=0)
        password_entry = CTkEntry(window, show="*")
        password_entry.grid(row=4, column=1)

        CTkLabel(window, text="Retype Password:").grid(row=5, column=0)
        rpassword_entry = CTkEntry(window, show="*")
        rpassword_entry.grid(row=5, column=1)

        status_label = CTkLabel(window)
        status_label.grid(row=7)

        signup_button = CTkButton(window, text="Sign Up", text_color=white, command=lambda :save_acc(first_name_entry,
                                     last_name_entry, email_entry, username_entry, password_entry, rpassword_entry
                                                                                   ,status_label))
        signup_button.grid(row=6, column=1)

    # Define a function to handle the login button
    def login():
        # Get the input values from the user
        username = username_entry.get()
        password = password_entry.get()

        if username==None or password==None:
            status_label.config(text="Incorrect username or password", fg="red")

        # Check if the user exists in the accounts table
        c.execute("SELECT * FROM accounts WHERE username = ? AND password = ?", (username, password))
        result = c.fetchone()

        if result:
            window.destroy()
            server()
        else:
            # Show a message for incorrect login information
            status_label.config(text="Incorrect username or password", fg="red")

    # Create the input fields
    username_label = CTkLabel(window, text="Username:")
    username_label.grid(row=0, column=0)
    username_entry = CTkEntry(window)
    username_entry.grid(row=0, column=1)

    password_label = CTkLabel(window, text="Password:")
    password_label.grid(row=1, column=0)
    password_entry = CTkEntry(window, show="*")
    password_entry.grid(row=1, column=1)

    # Create a label widget with clickable text
    label = CTkLabel(window, text="create an account", text_color="blue", cursor="hand2")
    label.grid(row=4,column=1)

    # Attach a callback function to the label
    label.bind("<Button-1>", lambda e: sign_up())

    login_button = CTkButton(window, text="Login", text_color=white, command=login)
    login_button.grid(row=2, column=1)
    status_label = CTkLabel(window, text="")
    status_label.grid(row=4)




# create labels to hold the products
CTkLabel(frame, text="Vehicle", font=myfont).grid(column=1, row=0, padx=30, pady=15)
CTkLabel(frame, text="Price", font=myfont).grid(column=2, row=0, padx=30, pady=15)
CTkLabel(frame, text="seats", font=myfont).grid(column=3, row=0, padx=30, pady=15)
CTkLabel(frame, text="Location", font=myfont).grid(column=4, row=0, padx=30, pady=15)
CTkButton(frame, text="Lessor Mode", text_color=white, font=myfont, command=lessor).grid(column=5, row=0, padx=30, pady=15)


# retrieve the product data from the database
connection = sqlite3.connect("cars.db")  # connect to the database
cursor = connection.cursor() #cursor is what make able to manipulate the data base

connection.commit()
cursor.execute("SELECT * FROM cars")
cars = cursor.fetchall()

# create a list to store the PhotoImage objects
photo_list = []

# create a label for each product
row = 1
for car in cars:

    # create a PhotoImage object from the image data
    image_data = car[1]
    if isinstance(image_data, str):
        image_data = image_data.encode()
    image = PIL.Image.open(BytesIO(image_data))
    photo = CTkImage(image, size=(160, 120))

    photo_list.append(photo)

    CTkLabel(frame, text="", image=photo_list[-1]).grid(column=0, row=row, padx=10, pady=15)

    # add the product data to the labels
    CTkLabel(frame, text=car[2], font=myfont).grid(column=1, row=row, padx=30, pady=15)
    CTkLabel(frame, text=car[3], font=myfont).grid(column=2, row=row, padx=30, pady=15)
    CTkLabel(frame, text=car[4], font=myfont).grid(column=3, row=row, padx=30, pady=15)
    CTkLabel(frame, text=car[5], font=myfont).grid(column=4, row=row, padx=30, pady=15)
    if car[6]==True:
        btn = CTkButton(frame, text="BOOK", width=20, text_color=white, font=myfont)
        btn.grid(column=5, row=row, padx=30, pady=15)
        btn.configure(command=lambda id=car[0]: book(id))
    else:
        CTkLabel(frame, text='not available', font=myfont).grid(column=5, row=row, padx=30, pady=15)
    row += 1



app.mainloop()