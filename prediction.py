# Install required libraries
# !pip install statsmodels

import pandas as pd
import sqlite3
from statsmodels.tsa.statespace.sarimax import SARIMAX

# Create a database connection
conn = sqlite3.connect('medicine_database.db')
cursor = conn.cursor()

# Assuming you have a database connection established

# Query the orders table to get historical data
cursor.execute("SELECT order_date, medication_name, dosage, SUM(quantity_ordered) as total_ordered FROM orders GROUP BY order_date, medication_name, dosage")
order_data = cursor.fetchall()

# Convert the query result into a DataFrame
df = pd.DataFrame(order_data, columns=["order_date", "medication_name", "dosage", "total_ordered"])

# Prepare data for SARIMA
df = df.rename(columns={"order_date": "ds", "total_ordered": "y"})
df['ds'] = pd.to_datetime(df['ds'])

# Create a model for each medication and dosage combination
models = {}
for name, group in df.groupby(['medication_name', 'dosage']):
    medication_name, dosage = name
    model = SARIMAX(group['y'], order=(1, 1, 1), seasonal_order=(1, 1, 1, 12))
    model_fit = model.fit(disp=False)

    # Store the model
    models[name] = model_fit

# Generate future dates
future_dates = pd.date_range(start=df['ds'].max(), periods=10, freq='D')

# Make forecasts for the next 10 days
forecast_data = []
for name, model in models.items():
    medication_name, dosage = name
    forecast = model.get_forecast(steps=10)
    forecast_df = forecast.summary_frame()
    forecast_df['medication_name'] = medication_name
    forecast_df['dosage'] = dosage
    forecast_data.append(forecast_df)

# Concatenate the forecasts
forecast_df = pd.concat(forecast_data)

# Assuming you have a table named 'forecasted_demand' in your database
forecast_df.to_sql('forecasted_demand', conn, if_exists='replace', index=False)

# Close the database connection
conn.close()
