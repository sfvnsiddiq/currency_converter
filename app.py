from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

API_URL = "https://api.exchangerate-api.com/v4/latest/{}"

@app.route("/")
def index():
    currencies = [
        "USD-US Dollar", "EUR-Euro", "INR-Indian Rupee", "JPY-Japanese Yen",
        "GBP-British Pound Sterling", "AUD-Australian Dollar", "CAD-Canadian Dollar",
        "CNY-Chinese Yuan Renminbi", "SAR-Saudi Riyal", "AED-UAE Dirham", "QAR-Qatari Riyal",
        "KWD-Kuwaiti Dinar", "BHD-Bahraini Dinar", "OMR-Omani Rial"
    ]
    return render_template("index.html", currencies=currencies)

@app.route("/convert", methods=["POST"])
def convert():
    data = request.get_json()
    base = data["base"]
    target = data["target"]
    amount = float(data["amount"])

    response = requests.get(API_URL.format(base))
    if response.status_code != 200:
        return jsonify({"error": "Failed to fetch rates"}), 500

    rates = response.json().get("rates", {})
    if target not in rates:
        return jsonify({"error": "Invalid target currency"}), 400

    rate = rates[target]
    result = amount * rate

    return jsonify({
        "converted": f"{amount:.2f} {base} = {result:.2f} {target}",
        "rate": rate
    })

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))  # Render sets PORT env variable
    app.run(host="0.0.0.0", port=port)
