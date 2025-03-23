import pandas as pd
import numpy as np
import os
from sklearn.linear_model import LinearRegression
import requests

CSV_FILE = "exchange_rates.csv"

# Fetch live exchange rates from API
def fetch_exchange_rates(base_currency="USD", target_currency="INR"):
    url = f"https://api.exchangerate-api.com/v4/latest/{base_currency}"
    response = requests.get(url)
    data = response.json()
    rates = data["rates"]
    
    if target_currency in rates:
        return rates[target_currency]
    return None

# Generate sample historical exchange rate data
def create_sample_data(base_currency="USD", target_currency="INR"):
    dates = pd.date_range(start="2024-01-01", periods=30, freq="D")
    rates = np.linspace(82.5, 83.5, num=30)  # Simulated increasing rates
    df = pd.DataFrame({"Date": dates, "Base_Currency": base_currency, "Target_Currency": target_currency, "Rate": rates})
    df.to_csv(CSV_FILE, index=False)
    print(f"Created {CSV_FILE} with sample data.")

# Load historical data for the selected currency pair
def load_data(base_currency="USD", target_currency="INR"):
    if not os.path.exists(CSV_FILE):
        create_sample_data(base_currency, target_currency)
    
    df = pd.read_csv(CSV_FILE)
    df["Date"] = pd.to_datetime(df["Date"]).map(pd.Timestamp.toordinal)
    
    # Filter data for selected currencies
    df = df[(df["Base_Currency"] == base_currency) & (df["Target_Currency"] == target_currency)]
    
    return df

# Train Linear Regression model
def train_model(base_currency="USD", target_currency="INR"):
    df = load_data(base_currency, target_currency)
    X = df["Date"].values.reshape(-1, 1)
    y = df["Rate"].values
    model = LinearRegression()
    model.fit(X, y)
    return model

# Predict future exchange rates for selected currency pair
def predict_exchange_rate(base_currency="USD", target_currency="INR", future_days=7):
    model = train_model(base_currency, target_currency)
    last_date = load_data(base_currency, target_currency)["Date"].max()
    future_dates = np.array([last_date + i for i in range(1, future_days + 1)]).reshape(-1, 1)
    predictions = model.predict(future_dates)
    
    # Format output
    predicted_rates = [{"Day": i+1, "Predicted Rate": round(predictions[i], 2)} for i in range(len(predictions))]
    return predicted_rates
