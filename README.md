# DriveByShare
**Drive By Share**

This project is a Car Management System that provides a graphical interface for managing car listings, bookings, and client information. The system allows you to add cars, display car details, save them into an SQLite database, and view the list of cars with the ability to delete or recover them. The interface is built using customtkinter and integrates various features, including QR code generation and secret code creation.

**Features:**

    * Add and Display Cars: Add new car entries with details such as name, price, seats, location, and availability. Display saved cars from the database with an option to delete or recover them.
    * Image Handling: Upload and display car images for each entry.
    * Database Integration: Save car details, including images, into an SQLite database.
    * Custom Widgets: Use a custom spinbox widget for selecting the number of seats.
    * QR Code Generation: Generate and save QR codes for car listings or client bookings.
    * Secret Code Generation: Generate a random 48-character secret code for car bookings.

**Libraries to Install:**

* pip install customtkinter
* pip install qrcode[pil]
* pip install Pillow


