import os
import requests
from dotenv import load_dotenv

# 한글 도시 이름을 영문으로 변환하는 딕셔너리
CITY_NAME_MAP = {
    "서울": "Seoul",
    "부산": "Busan",
    "인천": "Incheon",
    "대구": "Daegu",
    "광주": "Gwangju",
    "대전": "Daejeon",
    "울산": "Ulsan",
    "수원": "Suwon",
    "세종": "Sejong",
    "성남": "Seongnam",
    "고양": "Goyang",
    "용인": "Yongin",
    "창원": "Changwon",
    "청주": "Cheongju",
    "전주": "Jeonju",
    "천안": "Cheonan",
    "포항": "Pohang",
    "제주": "Jeju",
    "제주도": "Jeju"

}

def get_weather(city="서울"):
    """
    OpenWeatherMap API를 사용하여 특정 도시의 현재 날씨 정보를 가져옵니다.

    Args:
        city (str): 날씨를 조회할 도시 이름 (기본값: "서울")

    Returns:
        str: 날씨 정보 또는 오류 메시지
    """
    load_dotenv()
    api_key = os.getenv("OPENWEATHER_API_KEY")

    if not api_key:
        return "OpenWeatherMap API 키가 설정되지 않았습니다."

    # 지원하는 도시 목록
    supported_cities = list(CITY_NAME_MAP.keys())

    # 사용자가 입력한 도시가 지원 목록에 있는지 확인
    if city not in supported_cities:
        # 지원하지 않는 도시이거나, 도시 정보가 없는 경우 기본값 '서울'로 설정
        city = "서울"

    # 입력된 도시 이름(한글)을 영문으로 변환
    english_city = CITY_NAME_MAP.get(city)

    # API 요청 URL
    url = f"http://api.openweathermap.org/data/2.5/weather?q={english_city}&appid={api_key}&units=metric&lang=kr"

    try:
        response = requests.get(url)
        response.raise_for_status()  # 4xx/5xx 에러 발생 시 예외를 발생시킴
        data = response.json()

        if data["cod"] == 200:
            weather_description = data["weather"][0]["description"]
            temp = data["main"]["temp"]
            humidity = data["main"]["humidity"]
            wind_speed = data["wind"]["speed"]

            # 응답 메시지에는 원래 한글 도시 이름을 사용
            return f"현재 {city}의 날씨는 '{weather_description}'이며, 온도는 {temp}°C, 습도는 {humidity}%, 풍속은 {wind_speed}m/s 입니다."
        else:
            return f"'{city}'의 날씨 정보를 가져오는 데 실패했습니다: {data.get('message', '알 수 없는 오류')}"

    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            return f"'{city}' 도시를 찾을 수 없습니다. 다른 도시를 입력해주세요."
        return f"API 요청 중 HTTP 오류가 발생했습니다: {e}"
    except requests.exceptions.RequestException as e:
        return f"API 요청 중 오류가 발생했습니다: {e}"
    except Exception as e:
        return f"날씨 정보를 처리하는 중 오류가 발생했습니다: {e}"

if __name__ == '__main__':
    # 테스트를 위해 직접 실행할 경우
    print(get_weather(city="부산"))
    print(get_weather(city="서울"))
