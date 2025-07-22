import json
import spotipy
from langchain_openai import ChatOpenAI
from django.conf import settings
from home.lastfm_utils import get_similar_tracks_by_artist, get_tracks_by_tags
from home.mapping import MOOD_TAG_MAPPING as MOOD_TRANSLATION_MAP, GENRE_TAG_MAPPING, WEATHER_TO_MOOD_TAGS
from bot.utils import get_weather

# LLM 초기화
llm = ChatOpenAI(
    model="gpt-3.5-turbo",
    api_key=settings.OPENAI_API_KEY
)

def analyze_user_intent(user_message):
    prompt = f"""너는 사용자의 음악 추천 요청을 분석해서 intent와 keyword를 JSON으로 반환하는 분석기야.
    사용자가 \"{user_message}\"라고 입력했어.

    다음 intent 중 하나를 골라줘:
    - recommend_by_weather: 날씨에 어울리는 음악을 추천해달라는 요청
    - recommend_by_mood: 감정/기분 기반 음악 추천 요청
    - recommend_by_genre: 장르 기반 음악 추천 요청
    - recommend_by_keyword: 특정 키워드로 음악 검색 요청
    - search_music: 곡 제목이나 가수 검색 요청
    - general_conversation: 일반 대화

    'keywords'는 1개 이상이야. 단, '노래', '음악', '추천'처럼 일반적인 단어는 포함하지 마.
    감정(예: 슬픈), 장르(예: 케이팝), 분위기/스타일(예: 차분한) 등 의미 있는 키워드만 포함시켜.

    city는 사용자가 말한 도시가 있다면 꼭 넣고, 없다면 null로 해줘.
    **도시 예시**: 서울, 부산, 인천, 대전, 대구, 광주, 제주, 제주도, 수원, 고양, 성남, 용인, 울산, 세종, 창원, 청주, 전주, 천안, 포항 등

    응답은 반드시 JSON으로만 응답해:
    예)
    {{
      "intent": "recommend_by_weather",
      "keywords": [],
      "city": "부산"
    }}
    """

    try:
        response_content = _get_llm_response(prompt)
        print("LLM 응답:", response_content)
        if response_content.startswith("```json"):
            response_content = response_content[7:-3].strip()

        result = json.loads(response_content)
        if 'city' not in result:
            result['city'] = None
        if 'keywords' not in result:
            result['keywords'] = []

        return result
    except Exception as e:
        print(f"[오류] LLM 의도 분석 중 예외 발생: {e}")
        return {
            "intent": "general_conversation",
            "keywords": [],
            "city": None
        }

def normalize_keywords(keywords):
    mood_tag = None
    genre_tag = None

    for keyword in keywords:
        k = keyword.strip()

        if k in MOOD_TRANSLATION_MAP:
            mood_tag = MOOD_TRANSLATION_MAP[k]
        elif k in GENRE_TAG_MAPPING:
            genre_tag = GENRE_TAG_MAPPING[k]
        else:
            for m in MOOD_TRANSLATION_MAP:
                if m in k:
                    mood_tag = MOOD_TRANSLATION_MAP[m]
                    break
            for g in GENRE_TAG_MAPPING:
                if g in k:
                    genre_tag = GENRE_TAG_MAPPING[g]
                    break

    return mood_tag, genre_tag

def search_specific_music(sp_client, keyword, limit=5):
    try:
        results = sp_client.search(q=keyword, type='track', limit=limit, market='KR')
        if not results['tracks']['items']:
            return get_similar_tracks_by_artist(keyword, limit)

        tracks = []
        for track in results['tracks']['items']:
            tracks.append({
                'name': track['name'],
                'artist': ', '.join([a['name'] for a in track['artists']]),
                'url': track['external_urls']['spotify'],
                'album_image_url': track['album']['images'][0]['url'] if track['album']['images'] else None,
                'id': track['id']
            })
        return tracks
    except Exception as e:
        print(f"[오류] 특정 검색 중 오류 발생: {e}")
        return get_similar_tracks_by_artist(keyword, limit)

def get_recommendations_via_expanded_search(sp_client, initial_query, limit=5):
    try:
        search_result = sp_client.search(q=initial_query, type='track', limit=10, market='KR')
        if not search_result['tracks']['items']:
            return get_lastfm_fallback([initial_query], limit)

        for track in search_result['tracks']['items']:
            artist_id = track['artists'][0]['id']
            artist_info = sp_client.artist(artist_id)
            genres = artist_info.get('genres', [])
            if any('k-pop' in g or 'korean' in g for g in genres):
                genre_query = ' '.join([f'genre:"{g}"' for g in genres[:3]])
                final_results = sp_client.search(q=genre_query, type='track', limit=limit, market='KR')

                if not final_results['tracks']['items']:
                    return get_lastfm_fallback([initial_query], limit)

                return [
                    {
                        'name': track['name'],
                        'artist': ', '.join([a['name'] for a in track['artists']]),
                        'url': track['external_urls']['spotify'],
                        'album_image_url': track['album']['images'][0]['url'] if track['album']['images'] else None,
                        'id': track['id']
                    }
                    for track in final_results['tracks']['items']
                ]
        return get_lastfm_fallback([initial_query], limit)
    except Exception as e:
        print(f"[오류] 확장 검색 오류: {e}")
        return get_lastfm_fallback([initial_query], limit)

def get_lastfm_fallback(keywords, limit=5):
    print(f"[Fallback] Last.fm 태그 기반 추천 요청: '{keywords}'")
    mood_tag, genre_tag = normalize_keywords(keywords)
    print(f"[변환된 태그] mood: {mood_tag}, genre: {genre_tag}")
    return get_tracks_by_tags(mood_tag=mood_tag, genre_tag=genre_tag, limit=limit)

def normalize_weather_with_llm(raw_desc):
    print(f"[정규화 요청] 날씨 설명: {raw_desc}")
    prompt = f"""
    다음은 실제 날씨 API에서 받은 날씨 설명이야: "{raw_desc}"
    아래 정규화된 키 중 가장 유사한 것을 골라서 반환해줘:
    - 맑음
    - 흐림
    - 비
    - 눈
    - 천둥번개
    - 안개
    - 더움
    - 추움
    - 바람
    - 구름조금
    
    응답은 반드시 키 하나만 JSON 형식으로:
    {{"normalized": "흐림"}}
    """
    try:
        response = _get_llm_response(prompt)
        result = json.loads(response.strip("```json").strip("```"))
        return result.get("normalized")
    except:
        return None

def recommend_by_current_weather(city=None, limit=5):
    weather_info = get_weather(city=city)

    if "오류" in weather_info or "없습니다" in weather_info:
        return weather_info, []

    try:
        raw_desc = weather_info.split("의 날씨는 '")[1].split("'")[0]
        normalized = normalize_weather_with_llm(raw_desc)

        if not normalized or normalized not in WEATHER_TO_MOOD_TAGS:
            return f"현재 {city or '서울'}의 날씨는 '{raw_desc}'이지만, 이에 맞는 감정 태그가 없어요.", []

        mood_tags = WEATHER_TO_MOOD_TAGS[normalized]
        for mood_tag in mood_tags:
            tracks = get_tracks_by_tags(mood_tag=mood_tag, limit=limit)
            if tracks:
                break
        if not tracks:
            return f"{normalized} 분위기에 맞는 음악을 찾지 못했어요.", []
        
        city_name = city if city else "서울"
        return f"오늘 {city_name}의 날씨는 {normalized}이에요. 이런 음악은 어떠세요?", tracks

    except Exception as e:
        return f"날씨 분석 중 문제가 발생했어요: {e}", []

def _get_llm_response(prompt):
    import requests
    headers = {
        "Authorization": f"Bearer {settings.OPENAI_API_KEY}",
        "Content-Type": "application/json",
    }
    body = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": prompt}],
    }
    response = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers=headers,
        json=body
    )

    print("응답 상태 코드:", response.status_code)
    print("응답 본문:", response.text)

    try:
        return response.json()['choices'][0]['message']['content']
    except Exception as e:
        print("[LLM 응답 파싱 오류]", e)
        return "죄송해요. 답변을 생성하는 중 문제가 발생했어요."
