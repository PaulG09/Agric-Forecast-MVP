function getPrediction() {
	    const temperature = document.getElementById('temperature').value;
	    const rainfall = document.getElementById('rainfall').value;
	    const soilMoisture = document.getElementById('soil-moisture').value;

	    fetch('http://127.0.0.1:5000/predict', {
		    method: 'POST',
		    headers: {
			    'Content-Type': 'application/json'
		    },
		    body: JSON.stringify({
			    temperature: temperature,
			    rainfall: rainfall,
			    soil_moisture: soilMoisture
		    })
	    })
		.then(response => response.json())
		.then(data => {
		document.getElementById('prediction-result').innerHTML = `
		<h3>Predicted Crop Demand:</h3>
		<p>${data.predicted_demand}</p>
				`;
		})
		.catch(error => console.error('Error:', error));
}
