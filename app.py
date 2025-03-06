from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes to handle cross-origin requests

@app.route('/')
def home():
    return "Welcome to the Lifespan Prediction API!"

@app.route('/predict', methods=['POST'])
def predict_lifespan():
    try:
        # Get JSON data from the POST request
        data = request.get_json()

        # Check if all required fields are present
        required_fields = [
            'gender', 'age', 'occupation', 'sleep_duration', 
            'quality_of_sleep', 'physical_activity', 'stress_level', 
            'bmi_category', 'blood_pressure', 'heart_rate', 
            'daily_steps', 'sleep_disorder'
        ]
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing field: {field}"}), 400

        # Extract data for prediction (mock prediction)
        # You can replace this with your model's logic later
        age = int(data['age'])
        predicted_lifespan = 80  # Mocked value, replace with actual prediction logic

        return jsonify({
            'Predicted Lifespan': predicted_lifespan,
            'Received Data': data
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
