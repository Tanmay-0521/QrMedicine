# import tkinter as tk
# from tkinter import ttk, messagebox
# import sqlite3

# # Create a database connection
# conn = sqlite3.connect('medicine_database.db')
# cursor = conn.cursor()

# # Create medicines table if not exists
# cursor.execute('''CREATE TABLE IF NOT EXISTS medicines
#                 (id INTEGER PRIMARY KEY,
#                 name TEXT,
#                 dosage TEXT,
#                 expiry_date DATE,
#                 location TEXT,
#                 amount_available INTEGER,
#                 price_per_quantity REAL,
#                 bracket INTEGER)''')

# # Function to add a new medicine
# def add_medicine():
#     name = name_entry.get()
#     dosage = dosage_entry.get()
#     expiry_date = expiry_date_entry.get()
#     location = location_entry.get()
#     amount_available = amount_available_entry.get()
#     price_per_quantity = price_per_quantity_entry.get()
#     bracket = bracket_entry.get()  

#     # Check if medicine with the same name, dosage, and bracket already exists
#     cursor.execute("SELECT * FROM medicines WHERE name=? AND dosage=? AND bracket=?", (name, dosage, bracket))
#     existing_medicine = cursor.fetchone()

#     if existing_medicine:
#         # Update the existing medicine's amount_available
#         new_amount_available = int(existing_medicine[5]) + int(amount_available)
#         cursor.execute("UPDATE medicines SET amount_available=? WHERE id=?", (new_amount_available, existing_medicine[0]))
#     else:
#         # Insert a new entry
#         cursor.execute("INSERT INTO medicines (name, dosage, expiry_date, location, amount_available, price_per_quantity, bracket) VALUES (?, ?, ?, ?, ?, ?, ?)",
#                     (name, dosage, expiry_date, location, amount_available, price_per_quantity, bracket))

#     conn.commit()
#     messagebox.showinfo("Success", "Medicine added successfully!")

# # Function to delete a medicine
# def delete_medicine():
#     med_id = id_entry.get()
#     cursor.execute("DELETE FROM medicines WHERE id=?", (med_id,))
#     conn.commit()
#     messagebox.showinfo("Success", "Medicine deleted successfully!")

# # Function to search for a medicine
# def search_medicine():
#     name = search_name_entry.get()
#     cursor.execute("SELECT * FROM medicines WHERE name=?", (name,))
#     result = cursor.fetchall()

#     if result:
#         search_result.config(state=tk.NORMAL)
#         search_result.delete(1.0, tk.END)
#         search_result.insert(tk.END, result)
#         search_result.config(state=tk.DISABLED)
#     else:
#         search_result.config(state=tk.NORMAL)
#         search_result.delete(1.0, tk.END)
#         search_result.insert(tk.END, "Medicine not found.")
#         search_result.config(state=tk.DISABLED)

# # Create main window
# root = tk.Tk()
# root.title("Medicine Management App")
# root.geometry("400x500")

# # Create a frame for adding medicines
# add_frame = ttk.LabelFrame(root, text="Add Medicine")
# add_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

# # Labels and Entry Fields for adding a medicine
# tk.Label(add_frame, text="Name").grid(row=0, column=0, sticky="w")
# name_entry = ttk.Entry(add_frame)
# name_entry.grid(row=0, column=1, pady=(0, 10), sticky="w")

# tk.Label(add_frame, text="Dosage").grid(row=1, column=0, sticky="w")
# dosage_entry = ttk.Entry(add_frame)
# dosage_entry.grid(row=1, column=1, pady=(0, 10), sticky="w")

# tk.Label(add_frame, text="Expiry Date").grid(row=2, column=0, sticky="w")
# expiry_date_entry = ttk.Entry(add_frame)
# expiry_date_entry.grid(row=2, column=1, pady=(0, 10), sticky="w")

# tk.Label(add_frame, text="Location").grid(row=3, column=0, sticky="w")
# location_entry = ttk.Entry(add_frame)
# location_entry.grid(row=3, column=1, pady=(0, 10), sticky="w")

# tk.Label(add_frame, text="Amount Available").grid(row=4, column=0, sticky="w")
# amount_available_entry = ttk.Entry(add_frame)
# amount_available_entry.grid(row=4, column=1, pady=(0, 10), sticky="w")

# tk.Label(add_frame, text="Price per Quantity").grid(row=5, column=0, sticky="w")
# price_per_quantity_entry = ttk.Entry(add_frame)
# price_per_quantity_entry.grid(row=5, column=1, pady=(0, 10), sticky="w")

# tk.Label(add_frame, text="Bracket").grid(row=6, column=0, sticky="w")
# bracket_entry = ttk.Entry(add_frame)
# bracket_entry.grid(row=6, column=1, pady=(0, 10), sticky="w")

# ttk.Button(add_frame, text="Add Medicine", command=add_medicine).grid(row=7, columnspan=2)

# # Create a frame for deleting medicines
# delete_frame = ttk.LabelFrame(root, text="Delete Medicine")
# delete_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

# # Labels and Entry Fields for deleting a medicine
# tk.Label(delete_frame, text="Medicine ID to Delete").grid(row=0, column=0, sticky="w")
# id_entry = ttk.Entry(delete_frame)
# id_entry.grid(row=0, column=1, pady=(0, 10), sticky="w")

# ttk.Button(delete_frame, text="Delete Medicine", command=delete_medicine).grid(row=1, columnspan=2)

# # Create a frame for searching medicines
# search_frame = ttk.LabelFrame(root, text="Search Medicine")
# search_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

# # Labels and Entry Fields for searching a medicine
# tk.Label(search_frame, text="Name to Search").grid(row=0, column=0, sticky="w")
# search_name_entry = ttk.Entry(search_frame)
# search_name_entry.grid(row=0, column=1, pady=(0, 10), sticky="w")

# ttk.Button(search_frame, text="Search Medicine", command=search_medicine).grid(row=1, columnspan=2)

# # Result display for searching
# search_result = tk.Text(search_frame, height=4, width=40, state=tk.DISABLED)
# search_result.grid(row=2, columnspan=2, pady=(0, 10))

# # Start the main event loop
# root.mainloop()

# # Close the database connection
# conn.close()
import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

def create_database():
    conn = sqlite3.connect('medicine_database.db')
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS medicines
                    (id INTEGER PRIMARY KEY,
                    name TEXT,
                    dosage TEXT,
                    expiry_date DATE,
                    location TEXT,
                    amount_available INTEGER,
                    price_per_quantity REAL,
                    bracket INTEGER)''')

    conn.commit()
    conn.close()

def add_medicine():
    name = name_entry.get()
    dosage = dosage_entry.get()
    expiry_date = expiry_date_entry.get()
    location = location_entry.get()
    amount_available = amount_available_entry.get()
    price_per_quantity = price_per_quantity_entry.get()
    bracket = bracket_entry.get()  

    conn = sqlite3.connect('medicine_database.db')
    cursor = conn.cursor()

    cursor.execute("INSERT INTO medicines (name, dosage, expiry_date, location, amount_available, price_per_quantity, bracket) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (name, dosage, expiry_date, location, amount_available, price_per_quantity, bracket))

    conn.commit()
    conn.close()
    messagebox.showinfo("Success", "Medicine added successfully!")

def delete_medicine():
    med_id = id_entry.get()

    conn = sqlite3.connect('medicine_database.db')
    cursor = conn.cursor()

    cursor.execute("DELETE FROM medicines WHERE id=?", (med_id,))
    conn.commit()

    conn.close()
    messagebox.showinfo("Success", "Medicine deleted successfully!")

def search_medicine():
    name = search_name_entry.get()

    conn = sqlite3.connect('medicine_database.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM medicines WHERE name=?", (name,))
    result = cursor.fetchall()

    conn.close()

    if result:
        search_result.config(state=tk.NORMAL)
        search_result.delete(1.0, tk.END)
        search_result.insert(tk.END, result)
        search_result.config(state=tk.DISABLED)
    else:
        search_result.config(state=tk.NORMAL)
        search_result.delete(1.0, tk.END)
        search_result.insert(tk.END, "Medicine not found.")
        search_result.config(state=tk.DISABLED)

# Create main window
root = tk.Tk()
root.title("Medicine Management App")
root.geometry("400x500")

# Create database if not exists
create_database()

# Create a frame for adding medicines
add_frame = ttk.LabelFrame(root, text="Add Medicine")
add_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

# Labels and Entry Fields for adding a medicine
tk.Label(add_frame, text="Name").grid(row=0, column=0, sticky="w")
name_entry = ttk.Entry(add_frame)
name_entry.grid(row=0, column=1, pady=(0, 10), sticky="w")

# ... (continue adding labels and entry fields for dosage, expiry date, location, etc.)
tk.Label(add_frame, text="Dosage").grid(row=1, column=0, sticky="w")
dosage_entry = ttk.Entry(add_frame)
dosage_entry.grid(row=1, column=1, pady=(0, 10), sticky="w")

tk.Label(add_frame, text="Expiry Date").grid(row=2, column=0, sticky="w")
expiry_date_entry = ttk.Entry(add_frame)
expiry_date_entry.grid(row=2, column=1, pady=(0, 10), sticky="w")

tk.Label(add_frame, text="Location").grid(row=3, column=0, sticky="w")
location_entry = ttk.Entry(add_frame)
location_entry.grid(row=3, column=1, pady=(0, 10), sticky="w")

tk.Label(add_frame, text="Amount Available").grid(row=4, column=0, sticky="w")
amount_available_entry = ttk.Entry(add_frame)
amount_available_entry.grid(row=4, column=1, pady=(0, 10), sticky="w")

tk.Label(add_frame, text="Price per Quantity").grid(row=5, column=0, sticky="w")
price_per_quantity_entry = ttk.Entry(add_frame)
price_per_quantity_entry.grid(row=5, column=1, pady=(0, 10), sticky="w")

tk.Label(add_frame, text="Bracket").grid(row=6, column=0, sticky="w")
bracket_entry = ttk.Entry(add_frame)
bracket_entry.grid(row=6, column=1, pady=(0, 10), sticky="w")

ttk.Button(add_frame, text="Add Medicine", command=add_medicine).grid(row=7, columnspan=2)

# Create a frame for deleting medicines
delete_frame = ttk.LabelFrame(root, text="Delete Medicine")
delete_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

# Labels and Entry Fields for deleting a medicine
tk.Label(delete_frame, text="Medicine ID to Delete").grid(row=0, column=0, sticky="w")
id_entry = ttk.Entry(delete_frame)
id_entry.grid(row=0, column=1, pady=(0, 10), sticky="w")

ttk.Button(delete_frame, text="Delete Medicine", command=delete_medicine).grid(row=1, columnspan=2)

# Create a frame for searching medicines
search_frame = ttk.LabelFrame(root, text="Search Medicine")
search_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

# Labels and Entry Fields for searching a medicine
tk.Label(search_frame, text="Name to Search").grid(row=0, column=0, sticky="w")
search_name_entry = ttk.Entry(search_frame)
search_name_entry.grid(row=0, column=1, pady=(0, 10), sticky="w")

ttk.Button(search_frame, text="Search Medicine", command=search_medicine).grid(row=1, columnspan=2)

# Result display for searching
search_result = tk.Text(search_frame, height=4, width=40, state=tk.DISABLED)
search_result.grid(row=2, columnspan=2, pady=(0, 10))

# Start the main event loop
root.mainloop()
