package store.asiaepul.controller;

import java.util.Arrays;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.client.RestTemplate;

import store.asiaepul.entity.DataModel;
import store.asiaepul.entity.DataModel.ProgressData;

@Controller
public class DashboardController {

    @Autowired
    private RestTemplate restTemplate; // REST API 호출을 위한 RestTemplate 사용

    @GetMapping
    public String index(Model model) {
    	
    	Map<String, String> apiUrls = new HashMap<>();
    	apiUrls.put("http://localhost:8000/variance", "var");
    	apiUrls.put("http://localhost:8000/best-category", "cate");
    	apiUrls.put("http://localhost:8000/best-product", "prod");
    	apiUrls.put("http://localhost:8000/best-mart", "mart");
    	apiUrls.put("http://localhost:8000/peaktime", "peak");

    	for (Map.Entry<String, String> entry : apiUrls.entrySet()) {
    	    String url = entry.getKey();
    	    String attribute = entry.getValue();
    	    
    	    DataModel data = restTemplate.getForObject(url, DataModel.class);
    	    model.addAttribute(attribute, data);
    	}

        return "index";
    }
    
    @GetMapping("prediction")
    public String prediction(Model model) {
//    	String apiUrlProgressData = "http://localhost:8000/progress-data";
//    	
//    	ProgressData[] progressData = restTemplate.getForObject(apiUrlProgressData, ProgressData[].class);
//    	model.addAttribute("progressData", Arrays.asList(progressData));
        return "prediction";
    }

//    @GetMapping("/prediction")
//    public String prediction(@RequestParam(value = "modelName", required = false, defaultValue = "defaultModelName") String modelName, Model model) {
//        // 모델 이름에 따른 프로그레스 데이터 API URL
//        String apiUrl = "http://localhost:8000/progress-data";
//        if (!"defaultModelName".equals(modelName)) { // 기본 모델 이름이 아닌 경우 URL에 추가
//            apiUrl += "/" + modelName;
//        }
//        
//        try {
//            ResponseEntity<ProgressData[]> response = restTemplate.getForEntity(apiUrl, ProgressData[].class);
//            ProgressData[] progressData = response.getBody();
//            
//            if (progressData != null) { // API 호출 성공 및 데이터 확인
//                model.addAttribute("progressData", Arrays.asList(progressData));
//            }
//        } catch (Exception e) {
//            // 예외 처리 로직 (예: 로깅)
//            e.printStackTrace();
//        }
//        
//        return "prediction"; // 뷰 이름 반환
//    }
}