import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('cars.db')
cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS cars
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 image BLOB,
                 name TEXT,
                 price INTEGER,
                 seats INTEGER,
                 location TEXT,
                 availability BOOL,
                 time REAL,
                 client TEXT)''')


# Commit the changes
conn.commit()

# Close the connection
conn.close()
