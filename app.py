from flask import Flask, render_template, request, jsonify
import pandas as pd
import numpy as np
import plotly.express as px

app = Flask(__name__)
# Load crops from CSV
def load_crops():
    df = pd.read_csv('crops.csv')
    return df['Crop'].tolist()
# Route for homepage
@app.route('/')
def index():
    return render_template('index.html')

# API for forecasting
@app.route('/api/forecast', methods=['POST'])
def forecast():
    data = request.json
    crop = data.get('crop')
    timeframe = int(data.get('timeframe', 1))

    # Example: Random prediction (replace with real prediction logic)
    prices = np.random.randint(100, 200, size=(timeframe,))
    demand = np.random.randint(50, 100, size=(timeframe,))

    # Generate plotly chart for prices
    fig = px.line(x=list(range(1, timeframe+1)), y=prices, title=f'Price Forecast for {crop}')
    graphJSON = fig.to_json()

    return jsonify({
        "crop": crop,
        "timeframe": timeframe,
        "price_forecast": prices.tolist(),
        "demand_forecast": demand.tolist(),
        "chart": graphJSON
        })

    if __name__ == "__main__":
        app.run(debug=True)                                                 
