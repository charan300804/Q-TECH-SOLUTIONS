from flask import Flask, render_template, request
from currency_converter import fetch_exchange_rates, predict_exchange_rate

app = Flask(__name__)

# List of available currencies (for UI dropdown)
CURRENCIES = ["USD:United States Dollar 🇺🇸",
    "EUR: Euro (European Union) 🇪🇺",
    "INR: Indian Rupee 🇮🇳",
    "GBP: British Pound Sterling 🇬🇧",
    "JPY: Japanese Yen 🇯🇵",
    "CAD: Canadian Dollar 🇨🇦",
    "AUD: Australian Dollar 🇦🇺",
    "CNY: Chinese Yuan 🇨🇳",
    "CHF: Swiss Franc 🇨🇭",
    "SGD: Singapore Dollar 🇸🇬",
    "ZAR: South African Rand 🇿🇦",
    "BRL: Brazilian Real 🇧🇷",
    "MXN: Mexican Peso 🇲🇽",
    "HKD: Hong Kong Dollar 🇭🇰",
    "KRW: South Korean Won 🇰🇷",
    "NZD: New Zealand Dollar 🇳🇿",
    "THB: Thai Baht 🇹🇭",
    "RUB: Russian Ruble 🇷🇺"]

@app.route("/", methods=["GET", "POST"])
def index():
    converted_value = None
    predicted_rates = None
    rates = {}

    if request.method == "POST":
        base_currency = request.form.get("base_currency")
        target_currency = request.form.get("target_currency")
        amount = float(request.form.get("amount"))
        future_days = int(request.form.get("future_days", 7))

        # Fetch real-time exchange rate
        rate = fetch_exchange_rates(base_currency, target_currency)
        if rate:
            converted_value = round(amount * rate, 2)

        # Predict future exchange rates
        predicted_rates = predict_exchange_rate(base_currency, target_currency, future_days)

    return render_template("index.html", converted_value=converted_value, predicted_rates=predicted_rates, currencies=CURRENCIES)

if __name__ == "__main__":
    app.run(debug=True)

