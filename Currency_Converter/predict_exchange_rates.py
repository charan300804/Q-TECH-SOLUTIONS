import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

# Simulated exchange rate data (replace with real data)
data = {
    "Days": list(range(1, 31)),  # Simulating 30 days of data
    "Exchange_Rate": [80 + (i * 0.2) + np.random.randn() for i in range(30)]
}

df = pd.DataFrame(data)

# Prepare training data
X = df["Days"].values.reshape(-1, 1)  # Feature: Days
y = df["Exchange_Rate"].values  # Target: Exchange Rate

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train Linear Regression model
model = LinearRegression()
model.fit(X_train, y_train)

# Predict future exchange rates
future_days = np.array([[31], [32], [33], [34], [35]])  # Predict for next 5 days
predicted_rates = model.predict(future_days)

print("Predicted exchange rates for the next 5 days:", predicted_rates)

# Plot actual vs predicted exchange rates
plt.scatter(df["Days"], df["Exchange_Rate"], color="blue", label="Actual Rates")
plt.plot(future_days, predicted_rates, color="red", linestyle="dashed", label="Predicted Rates")
plt.xlabel("Days")
plt.ylabel("Exchange Rate")
plt.legend()
plt.show()
