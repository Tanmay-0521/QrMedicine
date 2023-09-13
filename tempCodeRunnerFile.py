import sqlite3

# Create a database connection
conn = sqlite3.connect('medicine_database.db')
cursor = conn.cursor()