import requests

# API URL (Ensure the API is running and accessible)
url = "https://lifespan-predictor.onrender.com/predict"

# Define the JSON data to send in the request
data = {
    "gender": "Male",
    "age": 25,
    "occupation": "Engineer",
    "sleep_duration": 7.0,
    "quality_of_sleep": 7,
    "physical_activity": 5,
    "stress_level": 5,
    "bmi_category": "Normal",
    "blood_pressure": "Normal",
    "heart_rate": 72,
    "daily_steps": 8000,
    "sleep_disorder": "No"
}

# Make the POST request
try:
    response = requests.post(url, json=data)
    response.raise_for_status()  # Raise an error for non-200 status codes
    
    print("HTTP Status Code:", response.status_code)
    print("✅ Prediction Response:", response.json())
except requests.exceptions.RequestException as e:
    print("❌ Error occurred:", e)