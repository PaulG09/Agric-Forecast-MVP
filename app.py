from flask import Flask, jsonify, request, render_template
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA

app = Flask(__name__)

# Load csv file
data_file = 'data/crops.csv'
data = pd.read_csv(data_file)

# Route to serve the homepage
@app.route('/')
def index():
    return render_template('index.html')

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
    # Check and convert PRODUCTION (Mt) to numeric
    time_series_data['PRODUCTION (Mt)'] = pd.to_numeric(time_series_data['PRODUCTION (Mt)'], errors='coerce')
    # Drop rows with NaN values
    time_series_data = time_series_data.dropna()
    # Debugging: Print the processed data and data types
    print("Processed Time Series Data:")
    print(time_series_data)
    print("Data Types:")
    print(time_series_data.dtypes)
    # Check if there's enough data to fit the model
    if len(time_series_data) < 2:
        return jsonify({'error': 'Not enough data to make a prediction.'}), 400
    # Prepare features and target
    X = time_series_data[['YEAR']]
    y = time_series_data['PRODUCTION (Mt)']

    # Split the data into training and test sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    # Create and train the Linear Regression model
    model = LinearRegression()
    model.fit(X_train, y_train)

    # Make a prediction for the next year
    next_year = time_series_data['YEAR'].max() + 1
    predicted_production = model.predict([[next_year]])[0]

    # Prepare the response
    response = {
            'crop': crop_name,
            'predicted_production_next_year': forecast,
            'historical_data': time_series_data.to_dict(orient='records')
            }
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
