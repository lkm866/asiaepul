import pandas as pd
from datetime import datetime, timedelta
from fastapi import FastAPI, Query, HTTPException
from starlette.middleware.cors import CORSMiddleware

from typing import List, Dict, Optional
from pydantic import BaseModel

import random

import asyncio


# from prisma import Prisma

app = FastAPI()

origins = [
    "http://localhost:3000",
    "http://localhost:8080"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class DataProcessor:
    def __init__(self):
        self.total_data = None
        self.yesterday_data = None
        self.today_data = None
        self.yesterday = datetime(2023, 12, 30)
        self.today = datetime(2023, 12, 31)

    def read_and_merge_data(self):
        if self.total_data is None:
            # 데이터 읽기 및 병합
            data_frames = [pd.read_csv(f"C:\\Pulmuone Fastapi\\data\\data{i}.csv") for i in range(10)]
            self.total_data = pd.concat(data_frames, ignore_index=True)
            # self.total_data['date'] = pd.to_datetime(self.total_data['date'])
            print(f"total_data: {self.total_data}")
            print("=================")
        return self.total_data

    def extract_yesterday_data(self):
        if self.yesterday_data is None:
            total_data = self.read_and_merge_data()
            total_data['date'] = pd.to_datetime(total_data['date'])  # 문자열을 datetime으로 변환
            start_of_day = datetime.combine(self.yesterday, datetime.min.time())
            end_of_day = datetime.combine(self.yesterday, datetime.max.time())
            self.yesterday_data = total_data[(total_data['date'] >= start_of_day) & (total_data['date'] <= end_of_day)]
            print(f"yestday_date: {self.yesterday_data}")
        return self.yesterday_data
    
    def extract_today_data(self):
        if self.today_data is None:
            total_data = self.read_and_merge_data()
            total_data['date'] = pd.to_datetime(total_data['date'])  # 문자열을 datetime으로 변환
            start_of_day = datetime.combine(self.today, datetime.min.time())
            end_of_day = datetime.combine(self.today, datetime.max.time())
            self.today_data = total_data[(total_data['date'] >= start_of_day) & (total_data['date'] <= end_of_day)]
            print(f"today_data: {self.today_data}")
        return self.today_data
    
    def get_variance(self, yestday_data, today_data):
        yesterday_tot_sum = yestday_data['tot'].sum()
        today_tot_sum = today_data['tot'].sum()
        
        change_rate = round(((today_tot_sum - yesterday_tot_sum) / yesterday_tot_sum) * 100, 2)
        symbol = '▲' if change_rate > 0 else '▼'
        change_rate_str = f"{symbol} {abs(change_rate)}%"
        print(data_processor.today)
        return change_rate_str
    
    def get_max_cate(self, today_data):
        max_cate = today_data.groupby('cate')['tot'].sum().idxmax()
        return max_cate

    def get_max_item(self, today_data):
        max_item = today_data.groupby(['cate', 'name'])['tot'].sum().idxmax()[1]
        return max_item

    def get_best_mart(self, today_data):
        today_data['mart'] = today_data['mart'].astype(str)
        best_mart = today_data.groupby('mart')['tot'].sum().idxmax()
        return best_mart

    
    def get_peak_time(self,today_data):
        today_data = today_data.copy()  # 복사본 생성
        today_data['date'] = pd.to_datetime(today_data['date'])
        peak_hour = today_data['date'].dt.hour.value_counts().idxmax()
        start_time = pd.to_datetime(f'{peak_hour}:00:00').strftime('%H:%M')
        end_time = (pd.to_datetime(f'{peak_hour}:00:00') + pd.Timedelta(hours=1)).strftime('%H:%M')
        peak_time = f"{start_time} ~ {end_time}"
        return peak_time


data_processor = DataProcessor()

@app.get("/variance")
def variance():
    yesterday_data = data_processor.extract_yesterday_data()
    today_data = data_processor.extract_today_data()
    result = data_processor.get_variance(yesterday_data, today_data)
    return {"variance": result}

@app.get("/best-category")
def best_category():
    today_data = data_processor.extract_today_data()
    result = data_processor.get_max_cate(today_data)
    return {"category": result}

@app.get("/best-product")
def best_product():
    today_data = data_processor.extract_today_data()
    result = data_processor.get_max_item(today_data)
    return {"product": result}

@app.get("/best-mart")
def best_mart():
    today_data = data_processor.extract_today_data()
    result = data_processor.get_best_mart(today_data)
    return {"mart": result}

@app.get("/peaktime")
def peaktime():
    today_data = data_processor.extract_today_data()
    result = data_processor.get_peak_time(today_data)
    return {"peakTime": result}


class MartData(BaseModel):
    categories: List[str]
    series: List[dict]

def get_mart_ranking(today_data):
    # Mart 별로 tot 열의 합을 구함
    mart_totals = today_data.groupby('mart')['tot'].sum().sort_values(ascending=True)

    # 상위 9개 Mart에 대한 tot 합을 1st, 2nd, 3rd, ..., 9th 변수에 저장
    top_mart_totals = mart_totals.head(9)

    # Mart와 해당 Mart의 순위를 저장할 딕셔너리 생성
    mart_ranking = {}
    for idx, (mart, total) in enumerate(top_mart_totals.items(), start=1):
        rank = f"{idx}st" if idx == 1 else f"{idx}nd" if idx == 2 else f"{idx}rd" if idx == 3 else f"{idx}th"
        mart_ranking[mart] = {rank: total}

    return mart_ranking


@app.get("/mart-rank", response_model=MartData)
async def get_bardata():
    today_data = data_processor.extract_today_data()
    mart_ranking = get_mart_ranking(today_data)

    # MartData 모델에 맞게 데이터 포맷팅
    categories = list(mart_ranking.keys())
    series = [{"value": list(values.values())[0]} for values in mart_ranking.values()]

    return MartData(categories=categories, series=series)

@app.get("/sales-volume")
def sales_volume():
    today_data = data_processor.extract_today_data()

    # today_data에서 code별 tot의 합계를 구하고 상위 5개를 선택합니다.
    top_codes_today = today_data.groupby('code')['tot'].sum().nlargest(5)
    
    sales_volume_data = []
    for rank, (code, today_tot) in enumerate(top_codes_today.items(), start=1):
        # 증감률 대신에 today_data에서 각 code의 tot의 합계 값을 입력합니다.
        # change_rate = abs(change_rate)  # 절대값으로 변환

        # 결과를 딕셔너리에 저장
        sales_top5 = {
            "rank": rank,
            "category": today_data.loc[today_data['code'] == code, 'cate'].iloc[0],
            "product": today_data.loc[today_data['code'] == code, 'name'].iloc[0],
            "amount": today_tot,  # 증감률 대신에 각 code의 tot의 합계 값을 입력합니다.
            # "change_rate": f"{symbol} {change_rate}%"  # 부호와 함께 증감률을 문자열 형식으로 저장
        }
        sales_volume_data.append(sales_top5)
    
    return sales_volume_data

@app.get("/rapid-change")
def get_top_changes():
    today_data = data_processor.extract_today_data()
    yesterday_data = data_processor.extract_yesterday_data()

    # today_data와 yesterday_data를 code로 그룹화하여 tot의 합계를 구합니다.
    today_totals = today_data.groupby('code')['tot'].sum()
    yesterday_totals = yesterday_data.groupby('code')['tot'].sum().loc[lambda x: x != 0]
    
    # 각 코드별 증감률을 계산합니다.
    changes = ((today_totals - yesterday_totals) / yesterday_totals) * 100
    
    # 증감률이 가장 큰 상위 5개를 선택합니다.
    top_changes = changes.nlargest(5)
    
    # 결과를 json 형식으로 변환합니다.
    result = []
    for rank, (code, change_rate) in enumerate(top_changes.items(), start=1):
        # 해당 코드의 정보를 추출합니다.
        category = today_data.loc[today_data['code'] == code, 'cate'].iloc[0]
        product = today_data.loc[today_data['code'] == code, 'name'].iloc[0]
        
        # 부호를 결정합니다.
        symbol = '▲' if change_rate > 0 else '▼'  # 양수이면 ▲, 음수이면 ▼
        
        # 결과를 딕셔너리로 구성합니다.
        entry = {
            "rank": rank,
            "category": category,
            "product": product,
            "changeRate": f"{symbol} {abs(change_rate):.2f}%"  # 부호와 함께 증감률을 문자열 형식으로 저장
        }
        result.append(entry)
    
    return result

class SalesData(BaseModel):
    categories: List[str]
    series: List[int]

@app.get("/sales-trend", response_model=SalesData)
async def get_sales_trend_chart_data():
    hours=[]
    for hour in range(13, 24):
        for minute in [30, 0]:
            if minute == 0:
                next_hour = hour + 1 if hour < 24 else 0  # 다음 시간의 시간 값 설정
                hours.append(f"{next_hour:02d}:00")
            else:
                hours.append(f"{hour:02d}:{minute:02d}")

    values = [125, 153, 142, 123, 116, 112, 140, 150, 146, 170, 180, 190, 207, 180, 166, 122, 111, 90, 76, 54, 40]
    
    return SalesData(categories=hours, series=values)

class PredictData(BaseModel):
    categories: List[str]
    series: List[Dict[str, List[int]]]

@app.get("/prediction", response_model=PredictData)
async def get_sales_trend_chart_data():
    dates = []
    
    start_date = datetime(2023, 1, 1)
    end_date = datetime(2023, 12, 31)

    extended_end_date = end_date + timedelta(days=40)

    date = start_date
    while date <= extended_end_date:
        year = str(date.year)[-2:]
        month = str(date.month).zfill(2)
        day = str(date.day).zfill(2)

        formatted_date = f"{year}.{month}.{day}"
        dates.append(formatted_date)

        date += timedelta(days=1)

    real_data = generate_real_data()
    predicted_data = generate_predicted_data()

    return PredictData(categories=dates, series=[
        {'realData': real_data},
        {'predictedData': predicted_data}
    ])


# 1년치의 더미 데이터를 생성하는 함수입니다.
def generate_real_data():
    data = []
    for i in range(365):
        # 수치를 엇비슷하게 만들기 위해 무작위 값을 사용합니다.
        random_value = random.randint(80, 250)
        data.append(random_value)

    return data

def generate_predicted_data():
    data = []
    for i in range(365 + 30):
        # 수치를 엇비슷하게 만들기 위해 무작위 값을 사용합니다.
        random_value = random.randint(80, 250)
        data.append(random_value)

    return data



@app.get("/products")
async def search_products(query: str = Query(default="")):
    print(query)
    filtered_products = []
    if query:
        # 쿼리와 일치하는 상품 필터링
        for i in range(26):
            product_name = chr(97 + i)
            if query.lower() in product_name:
                demand = random.randint(0, 99)
                variance = round(random.uniform(0, 100), 2)
                arrow = "▲" if variance > 0 else "▼"
                productObj = {
                    "productName": product_name,
                    "demand": demand,
                    "status": arrow,
                    "variance": str(variance) + '%'
                }
                filtered_products.append(productObj)
    else:
        # 모든 상품 반환
        for i in range(26):
            product_name = chr(97 + i)
            demand = random.randint(0, 99)
            variance = round(random.uniform(0, 100), 2)
            arrow = "▲" if variance > 0 else "▼"
            productObj = {
                "productName": product_name,
                "demand": demand,
                "status": arrow,
                "variance": str(variance) + '%'
            }
            filtered_products.append(productObj)

    return filtered_products

###################### progress Bar ######################
@app.get("/progress-data")
def get_progressData():
    return[
        {"title" : "1 weeks ago", "value" : 88.88},
        {"title" : "2 weeks ago", "value" : 58.23},
        {"title" : "3 weeks ago", "value" : 72.1},
        {"title" : "4 weeks ago", "value" : 49.82},
    ]
##########################################################
class AiModelData(BaseModel):
    name: str
    rank: Optional[int] = None
    total_models: Optional[int] = None
    accuracy: Optional[float] = None
    
models_info = {
    "CNN": AiModelData(name="CNN", rank=1, total_models=2, accuracy=92.5),
    "RNN": AiModelData(name="RNN", rank=2, total_models=2, accuracy=89.3)
}

@app.get("/aimodel-info/{model_name}", response_model=AiModelData)
def get_aimodel_info(model_name: str):
    if model_name in models_info:
        return models_info[model_name]
    else:
        raise HTTPException(status_code=404, detail="Model not found")