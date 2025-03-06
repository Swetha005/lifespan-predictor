from flask import Flask, render_template, request, jsonify
import pickle
import numpy as np

app = Flask(__name__)

# Load trained model
model = pickle.load(open("lifespan_model.pkl", "rb"))
scaler = pickle.load(open("scaler.pkl", "rb"))

@app.route("/")
def home():
    return render_template("index.html")  # Render HTML form for user input

@app.route("/predict", methods=["POST"])
def predict():
    try:
        # Get form data
        age = float(request.form["age"])
        sleep_hours = float(request.form["sleep_hours"])
        exercise_hours = float(request.form["exercise_hours"])
        smoking_status = float(request.form["smoking_status"])
        alcohol_consumption = float(request.form["alcohol_consumption"])
        diet_quality = float(request.form["diet_quality"])

        # Prepare input data
        input_data = np.array([[age, sleep_hours, exercise_hours, smoking_status, alcohol_consumption, diet_quality]])
        input_scaled = scaler.transform(input_data)  # Scale input data

        # Make prediction
        lifespan_prediction = model.predict(input_scaled)[0]

        return render_template("index.html", prediction_text=f"Predicted Lifespan: {lifespan_prediction:.2f} years")

    except Exception as e:
        return render_template("index.html", prediction_text=f"Error: {str(e)}")

if __name__ == "__main__":
    app.run(debug=True)
