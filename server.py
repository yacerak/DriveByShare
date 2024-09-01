from tools import *
import sqlite3
from customtkinter import *
import PIL.Image, PIL.ImageTk
from io import BytesIO

def server():
    myfont = ("Arial", 16)
    white = "#FFFFFF"
    app, frame = modern_window("server")
    app.geometry("1200x600")



    class Car:
        def __init__(self, image, name, price, seats, location, save, image_path):
            # store the car attributes
            self.image = image
            self.name = name
            self.price = price
            self.seats = seats
            self.location = location
            self.save = save
            self.image_path = image_path

        def car_row(self, row):

            # put the car attributes in a row on the frame
            self.image.grid(column=0, row=row, padx=30, pady=15)
            self.name.grid(column=1, row=row, padx=30, pady=15)
            self.price.grid(column=2, row=row, padx=30, pady=15)
            self.seats.grid(column=3, row=row, padx=30, pady=15)
            self.location.grid(column=4, row=row, padx=30, pady=15)
            self.save.grid(column=5, row=row, padx=30, pady=15)

            # configure the buttons
            self.image.configure(command=lambda: show_car_image(self.image, row, self.image_path))
            self.save.configure(
                command=lambda: save_car(self.name, self.price, self.seats, self.location, self.image_path, self.save,
                                         row))

    def create_car():
        # create the car attributes
        image = CTkButton(frame, text="+", font=myfont)
        name = CTkEntry(frame, font=myfont)
        price = CTkEntry(frame, font=myfont)
        seats = CTkSpinbox(frame, from_=1, to=7)
        location = CTkEntry(frame, font=myfont)
        save = CTkButton(frame, text="save", font=myfont, text_color=white)
        image_path = CTkLabel(frame, text="")
        car = Car(image, name, price, seats, location, save, image_path)
        row = 2
        while True:
            # get the widgets in the current row
            widgets = frame.grid_slaves(row=row, column=0)
            if not widgets:
                break
            row += 1
        car.car_row(row=row)



    def show_car_image(old_button, row, path):
        # get the image from the pc
        image_path = filedialog.askopenfilename(initialdir="C:/Users/yasse/OneDrive/Pictures",
                                                filetypes=(("all", "*.*"), ("PNG", "*.png"), ("JPEG", "*.jpeg")))
        new_label = CTkLabel(frame, text='✓')
        new_label.grid(column=0, row=row, padx=30, pady=15)

        # destroy the original button
        old_button.destroy()
        path.configure(text=image_path)

    def save_car(name, price, seats, location, image_path, save, row):
        car_name = name.get()
        car_price = float(price.get())
        car_seats = int(seats.get())
        car_location = location.get()
        img = PIL.Image.open(image_path.cget("text"))
        image_bytes = BytesIO()
        img.save(image_bytes, format='PNG')
        image_data = image_bytes.getvalue()

        cursor.execute("SELECT * FROM cars")
        cursor.fetchall()
        # add the products into the data base
        cursor.execute(
            "INSERT INTO cars (image, name, price, seats, location, availability) VALUES (?,?,?,?,?,?)",
            (image_data, car_name, car_price, car_seats, car_location, True))
        connection.commit()
        CTkButton(frame, text="saved", state=DISABLED).grid(row=row, column=5,  padx=30, pady=15)
        save.destroy()

    def recover(id, btn):
        cursor.execute("UPDATE cars SET time = ? WHERE id = ?", (0, id))
        cursor.execute("UPDATE cars SET availability = ? WHERE id = ?", (True, id))
        cursor.execute("UPDATE cars SET client = ? WHERE id = ?", (None, id))
        connection.commit()
        btn.destroy()

    def delete(id):
        cursor.execute("DELETE FROM cars WHERE id = ?", (id,))
        connection.commit()

        for widget in frame.grid_slaves(row=id):
            widget.destroy()

        print("car is deleted")


    def show_products():
        nframe = CTkToplevel(app)
        nframe.geometry("300x400")

        CTkLabel(nframe, text="car", font=myfont).grid(column=1, row=0, padx=30,pady=15)

        # retrieve the product data from the database
        connection = sqlite3.connect("cars.db")  # connect to the database
        cursor = connection.cursor()  # cursor is what make able to manipulate the data base

        connection.commit()
        cursor.execute("SELECT * FROM cars")
        cars = cursor.fetchall()

        if cars:
            # create a label for each product
            r = 1
            for car in cars:

                CTkLabel(nframe, text=car[2], font=myfont).grid(column=1, row=r, padx=30,
                                                                                             pady=15)
                CTkButton(nframe, text="delete", font=myfont,
                       command=lambda id=car[0]: delete(id)).grid(column=3, row=r, padx=30, pady=15)
                if car[6] == False:
                    rebtn = CTkButton(nframe, text="recover", font=myfont)
                    rebtn.config(command=lambda id=car[0], btn=rebtn: recover(id, btn))
                    rebtn.grid(column=4, row=r, padx=30, pady=15)
                else:
                    continue
                r += 1
        else:
            CTkLabel(nframe, text="there are no saved cars yet", font=("helvetica", 13), background="#C4DEDE").grid(
                column=1, row=2, padx=30, pady=15)


    def show_not():
        new_frame = CTkToplevel(app)
        new_frame.title('notifications')
        for i in range(len(notifications)):
            Label(new_frame, text=notifications[i]).pack()
        notifications.clear()

    connection = sqlite3.connect("cars.db")  # connect to the database
    cursor = connection.cursor()  # cursor is what make able to manipulate the data base

    notifications = []
    cursor.execute("SELECT * FROM cars")
    cars = cursor.fetchall()
    for car in cars:
        if car[-1] == False:
            notifications.append(f"the car of id={car[0]} is booked the client code is: {car[-1]}")
    connection.commit()

    # create a button to show saved products
    show = CTkButton(frame, text="Vehicles", font=myfont, command=show_products)

    show.grid(column=5, row=0, padx=5, pady=10)

    notif = CTkButton(frame, text="🔔", text_color=white, width=5, command=show_not)
    notif.grid(column=4, row=0, padx=5, pady=10)

    add_car = CTkButton(frame, text="add a new vehicle", text_color=white, font=myfont, command=create_car)
    add_car.grid(column=0, columnspan=2, row=0, padx=10, pady=10)

    CTkLabel(frame, text="image", font=myfont).grid(column=0, row=1, padx=5, pady=10)
    CTkLabel(frame, text="Vehicle", font=myfont).grid(column=1, row=1, padx=5, pady=10)
    CTkLabel(frame, text="PpH", font=myfont).grid(column=2, row=1, padx=5, pady=10)
    CTkLabel(frame, text="seats", font=myfont).grid(column=3, row=1, padx=5, pady=10)
    CTkLabel(frame, text="location", font=myfont).grid(column=4, row=1, padx=5, pady=10)

    first_row = create_car()

    # start the window
    app.mainloop()


