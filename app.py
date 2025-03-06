from flask import Flask, request, jsonify
import joblib

import numpy as np
from flask_cors import CORS  # To allow requests from HTML page

app = Flask(__name__)
CORS(app)  # Enable CORS for cross-origin requests

# Load trained model and encoders
model = joblib.load("lifespan_model.pkl")  # Use joblib instead of pickle
scaler = joblib.load(open("scaler.pkl", "rb"))
label_encoders = joblib.load(open("label_encoders.pkl", "rb"))

@app.route("/")
def home():
    return "Lifespan Prediction API is Running!"

@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.json

        # Convert categorical values using label encoders
        gender = label_encoders["gender"].transform([data["gender"]])[0]
        bmi_category = label_encoders["bmi_category"].transform([data["bmi_category"]])[0]
        blood_pressure = label_encoders["blood_pressure"].transform([data["blood_pressure"]])[0]
        sleep_disorder = label_encoders["sleep_disorder"].transform([data["sleep_disorder"]])[0]

        # Prepare features
        features = np.array([
            gender, data["age"], data["sleep_duration"], data["quality_of_sleep"], 
            data["physical_activity"], data["stress_level"], bmi_category, blood_pressure, 
            data["heart_rate"], data["daily_steps"], sleep_disorder
        ]).reshape(1, -1)

        # Scale input
        features_scaled = scaler.transform(features)

        # Predict lifespan
        predicted_lifespan = model.predict(features_scaled)[0]

        return jsonify({"Predicted Lifespan": round(predicted_lifespan, 2)})

    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(debug=True)
