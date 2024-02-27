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
    }
}

function updateProgressData(modelName) {
    fetch(`http://localhost:8000/progress-data/${modelName}`)
    .then(response => response.json())
    .then(data => {
        const progressContainer = document.querySelector('.prediction-calculation');
        progressContainer.innerHTML = '<h1 class="font-size:4 color:base-6 font-weight:600">예측 산출 가중치</h1>'; // 기존 내용을 제거하고 타이틀 추가
        data.forEach(progress => {
            const progressBarHTML = `
                <div class="progress-title">${progress.title}</div>
                <div class="progress-bar horizontal">
                    <div class="progress-track">
                        <div class="progress-fill" style="width: ${progress.value}%"></div>
                    </div>
                </div>
                <span class="progress-value">${progress.value}%</span>
            `;
            progressContainer.innerHTML += progressBarHTML; // 각 가중치 정보로 프로그레스바 추가
        });
    })
    .catch(error => {
        console.error('Error_progress data:', error);
    });
}
