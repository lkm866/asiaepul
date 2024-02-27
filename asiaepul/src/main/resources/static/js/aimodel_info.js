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

async function updateChartData(modelName) {
    const url = `http://localhost:8000/prediction11/${modelName}`; // 모델 이름에 따른 URL
    // const url = `http://localhost:8000/prediction11?model_name=${modelName}`; // 모델 이름에 따른 URL

    try {
        const response = await fetch(url);
        const chartData = await response.json();

        // 차트 업데이트 로직
        drawChart(chartData); // `drawChart` 함수를 차트 데이터와 함께 호출하여 차트를 업데이트
    } catch (error) {
        console.error('Error updating chart data:', error);
    }
}

function loadModelInfo() {
    var modelName = document.getElementById("modelSelect").value;
    if(modelName) {
        fetch(`http://localhost:8000/aimodel-info/${modelName}`)
        .then(response => response.json())
        .then(data => {
            // 받은 모델 정보를 페이지에 표시합니다.
            // document.getElementById("modelName").innerText = data.name;
            document.getElementById("modelRank").innerText = data.rank + " / ";
            document.getElementById("modelTotal").innerText = data.total_models;
            document.getElementById("modelAccuracy").innerText = data.accuracy + " %";
			
			document.querySelectorAll("#modelInfo dd span").forEach(span => {
                span.style.display = "inline";
            });
            document.getElementById("modelInfo").style.display = "grid";
            
            updateChartData(modelName);
        })
        .catch(error => {
            console.error('Error_model info:', error);
            alert("모델 정보를 가져오는 데 실패했습니다.");
        });
    } else {
        document.querySelectorAll("#modelInfo dd span").forEach(span => {
                span.style.display = "none";
            });
    }
}