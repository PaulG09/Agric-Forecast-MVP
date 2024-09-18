# Import necessary libraries
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import joblib

# Load the dataset (replace 'crop_data.csv' with your actual dataset path)
data = pd.read_csv('crop_data.csv')

# Features and target variable
X = data[['temperature', 'rainfall', 'soil_moisture']]
y = data['crop_demand']

# Split the data into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the model (Linear Regression)
model = LinearRegression()
model.fit(X_train, y_train)

# Save the trained model to a file
joblib.dump(model, 'crop_demand_model.pkl')

# Test the model (optional)
score = model.score(X_test, y_test)
print(f"Model R^2 score: {score:.2f}")
