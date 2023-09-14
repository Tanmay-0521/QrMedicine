import sqlite3
from datetime import datetime, timedelta
import pandas as pd

# Create a database connection
conn = sqlite3.connect('medicine_database.db')
cursor = conn.cursor()

# Calculate the date 30 days ago from today
end_date = datetime.now()
start_date = end_date - timedelta(days=1)

# Query the database for orders and availability in the last 30 days
cursor.execute("SELECT medicines.name, medicines.dosage, SUM(orders.quantity_ordered) as total_ordered, medicines.amount_available FROM medicines LEFT JOIN orders ON medicines.name = orders.medication_name AND medicines.dosage = orders.dosage AND orders.order_date BETWEEN ? AND ? GROUP BY medicines.name, medicines.dosage",
               (start_date, end_date))
order_data = cursor.fetchall()

if not order_data:
    print("No data available for the last 30 days.")
else:
    # Convert the query result into a DataFrame
    df = pd.DataFrame(order_data, columns=["medicine_name", "dosage", "total_ordered", "amount_available"])

    # Feature engineering: Calculate a priority score combining total_ordered and availability
    df["priority_score"] = df["total_ordered"] / (df["amount_available"] + 1)  # Adding 1 to avoid division by zero

    # Sort the DataFrame by priority_score in descending order
    df = df.sort_values(by="priority_score", ascending=False)

    # Get the most prioritized medicine
    most_prioritized_medicine = df.iloc[0]

    print(f"The most prioritized medicine in the last 30 days is: {most_prioritized_medicine['medicine_name']}")

# Close the database connection
conn.close()