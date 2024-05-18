import functions_framework
import logging
import json

class BMICalculator:
    def calculate_bmi(self, weight, height):
        """Calculate Body Mass Index (BMI) value."""
        if height <= 0 or weight <= 0:
            raise ValueError('Weight and height must be positive numbers.')
        return round(weight / (height ** 2), 2)

    def determine_weight_category(self, bmi):
        """Determine weight category based on BMI."""
        if bmi < 18.5:
            return "Underweight"
        elif bmi >= 18.5 and bmi < 24.9:
            return "Normal weight"
        elif bmi >= 25 and bmi < 29.9:
            return "Overweight"
        else:
            return "Obese"

class BMIService:
    def __init__(self, bmi_calculator):
        self.bmi_calculator = bmi_calculator

    def calculate_bmi_and_category(self, weight, height):
        """Calculate BMI and weight category."""
        bmi = self.bmi_calculator.calculate_bmi(weight, height)
        weight_category = self.bmi_calculator.determine_weight_category(bmi)
        return bmi, weight_category

bmi_calculator = BMICalculator()
bmi_service = BMIService(bmi_calculator)

@functions_framework.http
def calculate_bmi(request):
    """HTTP Cloud Function to calculate Body Mass Index (BMI).
    
    This function calculates the Body Mass Index (BMI) based on
    the weight (in kilograms) and height (in meters) provided in the
    HTTP request parameters.
    
    Args:
        request (flask.Request): The request object.
            <https://flask.palletsprojects.com/en/1.1.x/api/#incoming-request-data>
    
    Returns:
        The calculated Body Mass Index (BMI) and weight category.
    """
    try:
        request_json = request.get_json(silent=True)
        weight = float(request_json['weight'])
        height = float(request_json['height'])
        logging.info(f"Weight: {weight}, Height: {height}")
        # Calculate BMI and weight category
        bmi, weight_category = bmi_service.calculate_bmi_and_category(weight, height)
        logging.info(f"Weight: {bmi}, Height: {weight_category}")
        # Create JSON response
        response_data = {
            "bmi": bmi,
            "weight_category": weight_category
        }
        logging.info(f"Response data: {response_data}")
        # Return JSON response
        return json.dumps(response_data)
    
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        return json.dumps({"error": f"Error calculating BMI: {str(e)}"}), 500