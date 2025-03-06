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

        # Extract data for prediction
        age = int(data['age'])
        sleep_duration = int(data['sleep_duration'])
        quality_of_sleep = data['quality_of_sleep']
        physical_activity = data['physical_activity']
        stress_level = data['stress_level']
        bmi_category = data['bmi_category']
        heart_rate = int(data['heart_rate'])
        daily_steps = int(data['daily_steps'])
        sleep_disorder = data['sleep_disorder']

        # Initialize lifespan prediction (base value)
        predicted_lifespan = 80  # Default lifespan (for an average person)

        # Weighting factors for each feature
        gender_factor = {'Male': -2, 'Female': 2}  # Females tend to live longer
        age_factor = 0.1  # Decrease lifespan by 0.1 per year of age over 50
        sleep_factor = 0.5  # Improve lifespan by 0.5 for each hour of sleep
        sleep_quality_factor = {'Good': 2, 'Average': 0, 'Poor': -2}  # Quality of sleep effect
        activity_factor = {'Regular': 3, 'None': -3}  # Regular activity vs no activity
        stress_factor = {'Low': 2, 'Moderate': 0, 'High': -3}  # Stress levels
        bmi_factor = {'Normal': 2, 'Overweight': -2, 'Obese': -5}  # BMI categories
        blood_pressure_factor = {'Normal': 2, 'High': -3}  # Blood pressure levels
        heart_rate_factor = -0.1  # Decrease lifespan by 0.1 for every bpm over 80
        sleep_disorder_factor = {'Yes': -3, 'No': 0}  # Sleep disorder effect

        # Apply gender factor
        predicted_lifespan += gender_factor.get(data['gender'], 0)

        # Apply age factor (every year above 50 reduces lifespan)
        predicted_lifespan -= (age - 50) * age_factor if age > 50 else 0

        # Apply sleep duration (each hour of sleep adds lifespan)
        if sleep_duration < 6:
            predicted_lifespan -= 2  # Less than 6 hours of sleep
        elif sleep_duration > 9:
            predicted_lifespan -= 1  # More than 9 hours of sleep
        else:
            predicted_lifespan += sleep_duration * sleep_factor  # Between 6-9 hours is ideal

        # Apply sleep quality factor
        predicted_lifespan += sleep_quality_factor.get(quality_of_sleep, 0)

        # Apply physical activity factor
        predicted_lifespan += activity_factor.get(physical_activity, 0)

        # Apply stress level factor
        predicted_lifespan += stress_factor.get(stress_level, 0)

        # Apply BMI category factor
        predicted_lifespan += bmi_factor.get(bmi_category, 0)

        # Apply blood pressure factor
        predicted_lifespan += blood_pressure_factor.get(data['blood_pressure'], 0)

        # Apply heart rate factor
        if heart_rate > 80:
            predicted_lifespan -= (heart_rate - 80) * heart_rate_factor

        # Apply sleep disorder factor
        predicted_lifespan += sleep_disorder_factor.get(sleep_disorder, 0)

        # Apply daily steps as additional positive impact (every 1000 steps add lifespan)
        predicted_lifespan += daily_steps // 1000  # For example, 8000 steps would add 8 years

        # Return the predicted lifespan with the received data
        return jsonify({
            'Predicted Lifespan': round(predicted_lifespan, 1),
            'Received Data': data
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
