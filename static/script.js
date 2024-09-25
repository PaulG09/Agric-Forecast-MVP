ddEventListener("DOMContentLoaded", function () {
	    const cropSelect = document.getElementById("crop");
	    const forecastForm = document.getElementById("forecastForm");
	    const resultsDiv = document.getElementById("results");
	    const loadingDiv = document.getElementById("loading");
	    const chartCanvas = document.getElementById("chart").getContext("2d");

	async function loadCrops() {
		try {
			const response = await fetch('crops.csv');
			const data = await response.text();
			const rows = data.split('\n').slice(1);
			rows.forEach(row => {
				const columns = row.split(',')
				const cropName = columns[3].trim(); 
				const option = document.createElement("option");
				option.value = cropName;
				option.textContent = cropName;
				cropSelect.appendChild(option);
			});

		} catch (error) {
			console.error("Error loading crops:", error)
			alert("Failed to load crop options. Please try again later.");
		}
	}

	forecastForm.addEventListener("submit", async function (event) {
		event.preventDefault();
		resultsDiv.innerHTML = ""; 
		loadingDiv.style.display = "block";
		const selectedCrop = cropSelect.value;
		const selectedTimeframe = timeframe.value;
		try {
			const response = await fetch(`/api/forecast?crop=${selectedCrop}&timeframe=${selectedTimeframe}`);
			const result = await response.json();
			displayResults(result);
			plotChart(result);
		} catch (error) {
			console.error("Error fetching forecast:", error);
			alert("Failed to fetch forecast. Please try again later.");
		} finally {
			loadingDiv.style.display = "none";
		}
	});
	function displayResults(result) {
	resultsDiv.innerHTML = `
	<h2>Forecast Results for ${result.crop}</h2>
	<p>Projected Demand: ${result.demand} Mt</p>
	<p>Projected Price: $${result.price}</p>
			`;
	}
	function plotChart(data) {
		const chartData = {
			labels: data.dates,
			datasets: [{
				label: 'Projected Demand',
				data: data.demandValues,
				backgroundColor: 'rgba(76, 175, 80, 0.5)',
				borderColor: 'rgba(76, 175, 80, 1)',
				borderWidth: 1,
				fill: true,
			}]
		};

		const myChart = new Chart(chartCanvas, {
			type: 'line',
			data: chartData,
			options: {
				responsive: true,
				scales: {
					y: {
						beginAtZero: true,
					}
				}
			}
		});
	}

	loadCrops();
});
