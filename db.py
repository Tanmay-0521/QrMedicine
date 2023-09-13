import sqlite3

# Connect to the database
conn = sqlite3.connect('medicine_database.db')
c = conn.cursor()

# Modify the CREATE TABLE statement to include price_per_quantity and bracket columns
c.execute('''
    CREATE TABLE IF NOT EXISTS medicines
    (id INTEGER PRIMARY KEY,
    name TEXT,
    dosage TEXT,
    expiry_date DATE,
    location TEXT,
    amount_available INTEGER,
    price_per_quantity REAL,
    bracket TEXT)  -- Assuming bracket is a string identifier
''')
c.execute('''
    CREATE TABLE IF NOT EXISTS orders
    (id INTEGER PRIMARY KEY,
    order_date DATE,
    patient_name TEXT,
    doctor_name TEXT,
    medication_name TEXT,
    dosage TEXT,
    quantity_ordered INTEGER,
    FOREIGN KEY (medication_name, dosage) REFERENCES medicines(name, dosage))
''')
# Commit changes and close connection
conn.commit()
conn.close()
