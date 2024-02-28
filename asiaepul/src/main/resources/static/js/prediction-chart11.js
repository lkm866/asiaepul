document.addEventListener("DOMContentLoaded", async () => {
    const dom = document.getElementById('prediction-chart11');
    const myChart = echarts.init(dom, null, {
        renderer: 'canvas',
        useDirtyRect: false
    });
 
    
    async function drawChart(modelName) {
		// FastAPI 판매량 증감 추이 url
		const url = `http://localhost:8000/prediction11?model_name=${modelName}`;
		
		const response = await fetch(url);
		const chartData = await response.json();
		console.log(chartData);

	    const series = [
	        {
	            "name": "실제 수요",
	            "type": "line",
	            "data": chartData.series[0].realData
	        },
	        {
	            "name": "예측 수요",
	            "type": "line",
	            "data": chartData.series[1].predictedData
	        }
	    ];
	
	    const option = {
	        tooltip: {
	            trigger: 'axis',
	            axisPointer: {
	                type: 'cross',
	                crossStyle: {
	                    color: '#999'
	                }
	            }
	        },
	        toolbox: {
	            feature: {
	                dataView: { show: true, readOnly: false },
	                magicType: { show: true, type: ['line', 'bar'] },
	                restore: { show: true },
	                saveAsImage: { show: true }
	            }
	        },
	        legend: {
	            data: series.map(s => s.name)  // 동적으로 범례 데이터 설정
	        },
	        xAxis: [
	            {
	                type: 'category',
	                data: chartData.categories,
	                axisPointer: {
	                    type: 'shadow'
	                }
	            }
	        ],
	        yAxis: [
	            {
	                type: 'value',
	                name: '',
	            }
	        ],
	        dataZoom: [
	            {
	              type: 'inside',
	              start: 0,
	              end: 10
	            },
	            {
	              start: 0,
	              end: 10
	            }
	        ],
	        series: series.map(s => ({
	            ...s,
	            tooltip: {
	                valueFormatter: function(value) {
	                return value + ' box';  // 단위
	                }
	            },
	            symbol: 'none'
	        }))
	    };
	 
	    myChart.setOption(option);
	    
	    const dataSize = chartData.categories.length;
	    const startValue = Math.max(0, dataSize - 120); // 최근 10일을 보여주도록 설정, 데이터가 10개 미만인 경우는 처음부터 끝까지 보여줌
	    const endValue = dataSize - 1; // 마지막 인덱스
	
	    myChart.dispatchAction({
	        type: 'dataZoom',
	        startValue: startValue,
	        endValue: endValue
	    });
	    
	    window.addEventListener('resize', myChart.resize);
    }
    window.drawChart = drawChart; // drawChart 함수를 window 객체에 할당하여 전역에서 접근 가능
 
});

async function updateChartData(modelName) {
    const url = `http://localhost:8000/prediction11?model_name=${modelName}`; // 모델 이름에 따른 URL

    try {
        const response = await fetch(url);
        if (!response.ok) { // HTTP 상태 코드가 2xx가 아니면 에러로 간주
            throw new Error('Network response was not ok.'); // 커스텀 에러 메시지와 함께 예외를 발생시킵니다.
        }
        const chartData = await response.json();

        // 차트 업데이트 로직
        drawChart(chartData); // `drawChart` 함수를 차트 데이터와 함께 호출하여 차트를 업데이트
    } catch (error) {
        console.error('Error updating chart data:', error);
        alert("차트 데이터를 불러오는 데 실패했습니다. 자세한 오류를 콘솔에서 확인하세요.");
    }
}