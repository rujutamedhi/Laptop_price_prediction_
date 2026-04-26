from flask import Flask, request, jsonify
import pickle
import pandas as pd
import numpy as np
import re
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# ✅ Load full pipeline (not just model)
with open("laptop_price_model.pkl", "rb") as file:
    model = pickle.load(file)

# -------- HELPER FUNCTIONS -------- #

def convert_ram(ram):
    return float(re.search(r'(\d+)', str(ram)).group())

def convert_ssd(ssd):
    ssd = str(ssd)
    if "TB" in ssd:
        return float(re.search(r'(\d+)', ssd).group()) * 1024
    elif "GB" in ssd:
        return float(re.search(r'(\d+)', ssd).group())
    return None

def convert_screen_size(size):
    return float(re.search(r'(\d+\.?\d*)', str(size)).group())

# -------- ROUTE -------- #

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()

    try:
        # ✅ Only 5 features
        processed_data = {
            "Brand": data["Brand"].split()[0],
            "Processor Brand": data["Processor Brand"],
            "RAM": convert_ram(data["RAM"]),
            "SSD Capacity": convert_ssd(data["SSD Capacity"]),
            "Screen Size": convert_screen_size(data["Screen Size"])
        }

        # Convert to DataFrame
        user_df = pd.DataFrame([processed_data])

        # Predict (pipeline handles encoding)
        log_price = model.predict(user_df)

        # Convert back from log
        price = np.expm1(log_price)

        return jsonify({
            "Predicted Price": round(price[0], 2)
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 400


if __name__ == '__main__':
    app.run(debug=True)