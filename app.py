from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes to handle cross-origin requests

@app.route('/')
def home():
    # Serve index.html when the user accesses the home route
    return render_template('index.html')

def validate_data(data, required_fields):
    """Check if all required fields are in the data"""
    missing_fields = [field for field in required_fields if field not in data]
    return missing_fields

@app.route('/predict', methods=['POST'])
def predict_lifespan():
    try:
        # Get JSON data from the POST request
        data = request.get_json()

        # Define the required fields
        required_fields = [
            'gender', 'age', 'occupation', 'sleep_duration', 
            'quality_of_sleep', 'physical_activity', 'stress_level', 
            'bmi_category', 'blood_pressure', 'heart_rate', 
            'daily_steps', 'sleep_disorder'
        ]

        # Check if all required fields are present
        missing_fields = validate_data(data, required_fields)
        if missing_fields:
            return jsonify({"error": f"Missing fields: {', '.join(missing_fields)}"}), 400

        # Extract data for prediction and ensure it's in the correct format
        try:
            age = int(data['age'])
            sleep_duration = int(data['sleep_duration'])
            heart_rate = int(data['heart_rate'])
            daily_steps = int(data['daily_steps'])
        except ValueError:
            return jsonify({"error": "Invalid data type for one or more fields. Please check your input."}), 400

        quality_of_sleep = data['quality_of_sleep']
        physical_activity = data['physical_activity']
        stress_level = data['stress_level']
        bmi_category = data['bmi_category']
        sleep_disorder = data['sleep_disorder']

        # Initialize lifespan prediction (base value)
        predicted_lifespan = 80  # Default lifespan (for an average person)

        # Weighting factors for each feature
        gender_factor = {'Male': -2, 'Female': 2}
        age_factor = 0.1
        sleep_factor = 0.5
        sleep_quality_factor = {'Good': 2, 'Average': 0, 'Poor': -2}
        activity_factor = {'Regular': 3, 'None': -3}
        stress_factor = {'Low': 2, 'Moderate': 0, 'High': -3}
        bmi_factor = {'Normal': 2, 'Overweight': -2, 'Obese': -5}
        blood_pressure_factor = {'Normal': 2, 'High': -3}
        heart_rate_factor = -0.1
        sleep_disorder_factor = {'Yes': -3, 'No': 0}

        # Apply the factors based on the data
        predicted_lifespan += gender_factor.get(data['gender'], 0)
        predicted_lifespan -= (age - 50) * age_factor if age > 50 else 0
        if sleep_duration < 6:
            predicted_lifespan -= 2
        elif sleep_duration > 9:
            predicted_lifespan -= 1
        else:
            predicted_lifespan += sleep_duration * sleep_factor
        predicted_lifespan += sleep_quality_factor.get(quality_of_sleep, 0)
        predicted_lifespan += activity_factor.get(physical_activity, 0)
        predicted_lifespan += stress_factor.get(stress_level, 0)
        predicted_lifespan += bmi_factor.get(bmi_category, 0)
        predicted_lifespan += blood_pressure_factor.get(data['blood_pressure'], 0)
        if heart_rate > 80:
            predicted_lifespan -= (heart_rate - 80) * heart_rate_factor
        predicted_lifespan += sleep_disorder_factor.get(sleep_disorder, 0)
        predicted_lifespan += daily_steps // 1000  # Adding years for daily steps

        # Return the predicted lifespan with the received data
        return jsonify({
            'Predicted Lifespan': round(predicted_lifespan, 1),
            'Received Data': data
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
