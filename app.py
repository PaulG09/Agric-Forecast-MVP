from flask import Flask, jsonify, request, render_template
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA

app = Flask(__name__)

#Load csv file
data_file = 'data/crops.csv'
data = pd.read_csv(data_file)

# Route to serve the homepage
@app.route('/')
def index():
    return render_template('index.html')

# Endpoint to get crop names
@app.route('/api/crops', methods=['GET'])
def get_crops():
    # Get unique crop names from the dataset
    crops_list = data['CROP'].unique()
    return jsonify(crops_list.tolist())
# Endpoint to predict production
@app.route('/api/predict', methods=['POST'])
def predict():
    # Get crop name and timeframe from the request
    crop_name = request.json.get('crop')
    timeframe = request.json.get('timeframe')  # This could be a year or range

    # Filter the data based on user input
    filtered_data = data[data['CROP'] == crop_name]
    if filtered_data.empty:
        return jsonify({'error': 'No data found for the specified crop.'}), 404
    # Prepare the data for time series analysis
    time_series_data = filtered_data.groupby('YEAR')['PRODUCTION (Mt)'].sum().reset_index()
    # Fit an ARIMA model (you can adjust the (p,d,q) parameters as needed)
    model = ARIMA(time_series_data['PRODUCTION (Mt)'], order=(1, 1, 1)) 
    # Example parameters
    model_fit = model.fit()
    # Make a prediction for the next year
    forecast = model_fit.forecast(steps=1)[0]
    # Prepare the response
    response = {
            'crop': crop_name,
            'predicted_production_next_year': forecast,
            'historical_data': time_series_data.to_dict(orient='records')
            }
    return jsonify(response)
if __name__ == '__main__':
    app.run(debug=True)
