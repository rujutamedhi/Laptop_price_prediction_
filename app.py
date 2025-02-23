import pickle
import pandas as pd
import numpy as np

# Load trained model
with open("laptop_price_model.pkl", "rb") as file:
    loaded_model = pickle.load(file)

# Load feature names used during training
train_columns = loaded_model.feature_names_in_

# Load scaler if used
try:
    with open("scaler.pkl", "rb") as file:
        scaler = pickle.load(file)
    scaling_used = True
except FileNotFoundError:
    scaling_used = False

# # Example input (Modify as per user requirement)
# # user_input = {
# #     "Brand": "ASUS",
# #     "Operating System": "Windows 11 Home",
# #     "Processor Name": "Core i5",
# #     "Storage Type": "SSD",
# #     "SSD": "Yes",
# #     "Screen Size": 15.6,
# #     "Resolution_Width": 2880,
# #     "Resolution_Height": 1620,
# #     "Total_Pixels": 2880 * 1620,
# #     "Aspect_Ratio": 2880 / 1620,
# #     "Processor Brand": "Intel",
# #     "RAM": "16 GB",
# #     "RAM Type": "DDR5",
# #     "SSD Capacity": "512 GB",
# #     "Touchscreen": "Yes",
# #     "Type": "Thin and Light Laptop"
# # }
# # user_input = {
# #     "Brand": "Acer",
# #     "Operating System": "Windows 11 Home",
# #     "Processor Name": "Core i5",
# #     "Storage Type": "SSD",
# #     "SSD": "Yes",
# #     "Screen Size": 15.6,
# #     "Resolution_Width": 1920,
# #     "Resolution_Height": 1080,
# #     "Total_Pixels": 1920 * 1080,
# #     "Aspect_Ratio": 1920 / 1080,
# #     "Processor Brand": "Intel",
# #     "RAM": "16 GB",
# #     "RAM Type": "DDR4",
# #     "SSD Capacity": "512 GB",
# #     "Touchscreen": "No",
# #     "Type": "Gaming Laptop"
# # }

# user_input = {
#     "Brand": "Asus",
#     "Operating System": "Windows 11 Home",
#     "Processor Name": "Core i3",
#     "Storage Type": "SSD",
#     "SSD": "Yes",
#     "Screen Size": 15.6,
#     "Resolution_Width": 1920,
#     "Resolution_Height": 1080,
#     "Total_Pixels": 1920 * 1080,
#     "Aspect_Ratio": 1920 / 1080,
#     "Processor Brand": "Intel",
#     "RAM": "8 GB",
#     "RAM Type": "DDR4",
#     "SSD Capacity": "512 GB",
#     "Touchscreen": "No",
#     "Type": "Thin and Light Laptop"
# }

# # Convert input to DataFrame
# user_df = pd.DataFrame([user_input])

# # Apply same transformations as training
# # Convert categorical variables using get_dummies()
# categorical_columns = ["Brand", "Operating System", "Processor Name", "Storage Type", "SSD",
#                        "Processor Brand", "RAM", "RAM Type", "SSD Capacity", "Touchscreen", "Type"]

# user_df = pd.get_dummies(user_df, columns=categorical_columns)

# # Add missing columns from train data
# for col in train_columns:
#     if col not in user_df.columns:
#         user_df[col] = False  # Assign False (0) for missing categories

# # Ensure column order is the same as training
# user_df = user_df[train_columns]

# # Apply scaling if used
# if scaling_used:
#     user_df = scaler.transform(user_df)

# # Predict log-transformed price
# log_price_pred = loaded_model.predict(user_df)

# # Convert back from log scale
# predicted_price = np.expm1(log_price_pred)

# print("Predicted Laptop Price:", round(predicted_price[0], 2))


# if __name__ == '__main__':
#     app.run(debug=True)
from flask import Flask, request, jsonify
import pickle
from flask_cors import CORS
import pandas as pd
import numpy as np

app = Flask(__name__)
CORS(app) 

# # Load trained model
# with open("laptop_price_model.pkl", "rb") as file:
#     loaded_model = pickle.load(file)

# # Load feature names used during training
# train_columns = loaded_model.feature_names_in_

# # Load scaler if used
# try:
#     with open("scaler.pkl", "rb") as file:
#         scaler = pickle.load(file)
#     scaling_used = True
# except FileNotFoundError:
#     scaling_used = False

@app.route('/predict', methods=['POST'])
def predict():
    print("Receivedd data")
    data = request.get_json()
    # Standardize keys to match frontend naming
    key_map = {
        "Operating_System": "Operating System",
        "Storage_Type": "Storage Type",
        "SSD_Capacity": "SSD Capacity",
        "Screen_Resolution": "Screen Resolution",
        "Screen_Size": "Screen Size",
        "Processor_Brand": "Processor Brand",
        "RAM_Type": "RAM Type",
    }
    # print(data)
    data["SSD"] = "Yes"
    # Rename keys if needed
    data = {key_map.get(k, k): v for k, v in data.items()}
    print(data)
    # Extract resolution width and height
    if "Screen Resolution" in data:
        try:
            print("resolution reached")
            resolution_width, resolution_height = map(int, data["Screen Resolution"].split(" X "))
            data["Resolution_Width"] = resolution_width
            data["Resolution_Height"] = resolution_height
            data["Total_Pixels"] = resolution_width * resolution_height
            data["Aspect_Ratio"] = resolution_width / resolution_height
            data["Brand"]="Asus"
        except ValueError:
            return jsonify({"error": "Invalid screen resolution format. Use 'WIDTH X HEIGHT'"}), 400
    
    # Convert input to DataFrame
    user_df = pd.DataFrame([data])
    print(user_df)
    # Apply same transformations as training
    # Convert categorical variables using get_dummies()
    categorical_columns = ["Brand", "Operating System", "Processor Name", "Storage Type", "SSD",
                        "Processor Brand", "RAM", "RAM Type", "SSD Capacity", "Touchscreen", "Type"]

    user_df = pd.get_dummies(user_df, columns=categorical_columns)

    # Add missing columns from train data
    for col in train_columns:
        if col not in user_df.columns:
            user_df[col] = False  # Assign False (0) for missing categories

    # Ensure column order is the same as training
    user_df = user_df[train_columns]

    # Apply scaling if used
    if scaling_used:
        user_df = scaler.transform(user_df)

    # Predict log-transformed price
    log_price_pred = loaded_model.predict(user_df)

    # Convert back from log scale
    predicted_price = np.expm1(log_price_pred)
    print(predicted_price)
    return jsonify({"Predicted Price": round(predicted_price[0], 2)})

if __name__ == '__main__':
    app.run(debug=True)
