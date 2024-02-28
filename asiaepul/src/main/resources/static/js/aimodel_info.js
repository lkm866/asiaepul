document.addEventListener('DOMContentLoaded', function() {
	fetch('http://localhost:8000/aimodel-name')
		.then(response => response.json())
		.then(data => {
			const selectElement = document.getElementById('modelSelect');
			data.forEach(modelName => {
				const option = new Option(modelName, modelName);
				selectElement.add(option);
			});
		})
		.catch(error => console.error('Error_model names:', error));
});

function loadModelInfo() {
	var modelName = document.getElementById("modelSelect").value;
	if (modelName) {
		fetch(`http://localhost:8000/aimodel-info/${modelName}`)
			.then(response => response.json())
			.then(data => {
				// document.getElementById("modelName").innerText = data.name;
				document.getElementById("modelRank").innerText = data.rank + " / ";
				document.getElementById("modelTotal").innerText = data.total_models;
				document.getElementById("modelAccuracy").innerText = data.accuracy + " %";

				document.querySelectorAll("#modelInfo dd span").forEach(span => {
					span.style.display = "inline";
				});
				document.getElementById("modelInfo").style.display = "grid";

				window.drawChart(modelName);

				updateProgressData(modelName);
			})
			.catch(error => {
				console.error('Error_model info:', error);
				alert("모델 정보를 가져오는 데 실패했습니다.");
			});
	} else {
		document.querySelectorAll("#modelInfo dd span").forEach(span => {
			span.style.display = "none";
		});
		document.querySelectorAll("#modelInfo dd span").forEach(span => {

			span.style.display = "none";

		});
		document.getElementById("modelRank").innerText = "";
		document.getElementById("modelTotal").innerText = "";
		document.getElementById("modelAccuracy").innerText = "";

		resetChart();
		resetProgressData();
	}
}

function updateProgressData(modelName) {
	fetch(`http://localhost:8000/progress-data/${modelName}`)
		.then(response => response.json())
		.then(data => {
			const mainProgressContainer = document.querySelector('.prediction-calculation');
			mainProgressContainer.innerHTML = ''; 
			
			const title = document.createElement('h1');
			title.className = 'font-size:4 color:base-6 font-weight:600'; 
			title.textContent = '예측 산출 가중치';
			mainProgressContainer.appendChild(title);

			data.forEach(progress => {
				// 각 progress 항목에 대한 독립적인 container 생성
				const progressContainer = document.createElement('div');
				progressContainer.className = 'progress-container';

				const progressTitle = document.createElement('div');
				progressTitle.className = 'progress-title';
				progressTitle.textContent = progress.title;

				const progressBar = document.createElement('div');
				progressBar.className = 'progress-bar';

				const progressTrack = document.createElement('div');
				progressTrack.className = 'progress-track';

				const progressFill = document.createElement('div');
				progressFill.className = 'progress-fill';
				progressFill.style.width = `${progress.value}%`;

				const progressValue = document.createElement('span');
				progressValue.className = 'progress-value';
				progressValue.textContent = `${progress.value}%`;

				progressTrack.appendChild(progressFill);
				progressBar.appendChild(progressTrack);
				progressContainer.appendChild(progressTitle);
				progressContainer.appendChild(progressBar);
				progressContainer.appendChild(progressValue);

				mainProgressContainer.appendChild(progressContainer);
			});
		})
		.catch(error => {
			console.error('Error fetching progress data:', error);
		});
}

function resetChart() {
	const dom = document.getElementById('prediction-chart11');
	if (dom) {
		const myChart = echarts.getInstanceByDom(dom) || echarts.init(dom);
		myChart.clear();
	}
}

function resetProgressData() {
	const mainProgressContainer = document.querySelector('.prediction-calculation');
	if (mainProgressContainer) {
 		const title = mainProgressContainer.querySelector('h1');
		mainProgressContainer.innerHTML = '';
		if (title) {
			mainProgressContainer.appendChild(title);
		}
	}
}