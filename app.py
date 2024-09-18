from flask import Flask, request, jsonify
import joblib
import numpy as np

app = Flask(__name__)

# Load the saved machine learning model
model = joblib.load('crop_demand_model.pkl')

@app.route('/predict', methods=['POST'])
def predict_demand():
        # Get the JSON data from the POST request
        data = request.get_json()
        # Extract the input values from the JSON
        temperature = data.get('temperature')
        rainfall = data.get('rainfall')
        soil_moisture = data.get('soil_moisture')
        # Handle missing input values
        if not temperature or not rainfall or not soil_moisture:
            return jsonify({"error": "Missing input data"}), 400
        # Prepare the input data for prediction
        input_data = np.array([[float(temperature), float(rainfall), float(soil_moisture)]])
        # Make the prediction using the trained model
        predicted_demand = model.predict(input_data)[0]
        # Return the predicted demand as JSON
        return jsonify({"predicted_demand": f"{predicted_demand:.2f} tonnes"})
    if __name__ == '__main__':
        # Run the Flask app
        app.run(debug=True)                                                                    
