function loadModelInfo() {
    var modelName = document.getElementById("modelSelect").value;
    if(modelName) {
        fetch(`http://localhost:8000/aimodel-info/${modelName}`)
        .then(response => response.json())
        .then(data => {
            // 받은 모델 정보를 페이지에 표시합니다.
            document.getElementById("modelName").innerText = data.name;
            document.getElementById("modelRank").innerText = data.rank + " / ";
            document.getElementById("modelTotal").innerText = data.total_models;
            document.getElementById("modelAccuracy").innerText = data.accuracy + " %";

            // 모델 정보 섹션을 표시합니다.
            // document.getElementById("modelInfo").style.display = "block";
        })
        .catch(error => {
            console.error('Error fetching model info:', error);
            //alert("모델 정보를 가져오는 데 실패했습니다.");
            // 모델 정보 섹션을 숨깁니다.
            // document.getElementById("modelInfo").style.display = "none";
        });
    } else {
        // 선택되지 않은 경우, 모델 정보 섹션을 숨깁니다.
        // document.getElementById("modelInfo").style.display = "none";
    }
}
