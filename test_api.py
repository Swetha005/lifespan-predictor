import unittest
import json
from app import app  # Import the Flask app from app.py

class TestLifespanPredictionAPI(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Set up the test client for the Flask app"""
        cls.client = app.test_client()

    def test_predict_lifespan(self):
        # Test input data
        input_data = {
            "gender": "Male",
            "age": 30,
            "occupation": "Software Engineer",
            "sleep_duration": 7,
            "quality_of_sleep": "Good",
            "physical_activity": "Regular",
            "stress_level": "Low",
            "bmi_category": "Normal",
            "blood_pressure": "Normal",
            "heart_rate": 70,
            "daily_steps": 8000,
            "sleep_disorder": "No"
        }

        # Send a POST request to the '/predict' endpoint
        response = self.client.post('/predict', json=input_data)

        # Assert that the response code is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Assert that the response contains the 'Predicted Lifespan' field
        response_data = json.loads(response.data)
        self.assertIn('Predicted Lifespan', response_data)
        self.assertEqual(response_data['Predicted Lifespan'], 80)

    def test_missing_data(self):
        # Test missing data (age field is missing)
        input_data = {
            "gender": "Male",
            "occupation": "Software Engineer",
            "sleep_duration": 7,
            "quality_of_sleep": "Good",
            "physical_activity": "Regular",
            "stress_level": "Low",
            "bmi_category": "Normal",
            "blood_pressure": "Normal",
            "heart_rate": 70,
            "daily_steps": 8000,
            "sleep_disorder": "No"
        }

        # Send a POST request to the '/predict' endpoint
        response = self.client.post('/predict', json=input_data)

        # Assert that the response code is 400 (Bad Request) because age is missing
        self.assertEqual(response.status_code, 400)

        # Assert that the error message indicates missing 'age'
        response_data = json.loads(response.data)
        self.assertIn("error", response_data)
        self.assertEqual(response_data["error"], "Missing field: age")

if __name__ == '__main__':
    unittest.main()
