import json
import spotipy
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage
from django.conf import settings # Django settings 임포트

# LLM 초기화 (settings.py에서 API 키를 가져오도록 수정)
llm = ChatOpenAI(
    model="gpt-3.5-turbo",
    api_key=settings.OPENAI_API_KEY
)

def analyze_user_intent(user_message):
    """
    LLM을 사용하여 사용자의 의도를 분석하고, 그에 맞는 키워드나 검색어를 생성합니다.
    """
    prompt = f"""You are an intelligent intent analyzer for a Korean music chatbot. Your primary goal is to understand what the user wants and provide the correct parameters for the next step. The user is Korean.

Analyze the user's message: '{user_message}'

First, determine the user's intent. There are three possible intents:
1.  `specific_search`: The user is asking for a specific song, artist, or album. (e.g., "아이유 노래 찾아줘", "방탄소년단 다이너마이트")
2.  `exploratory_recommendation`: The user is describing a mood, situation, or genre and wants a recommendation. (e.g., "슬픈 노래 추천해줘", "운동할 때 듣기 좋은 신나는 음악")
3.  `general_conversation`: The user is just chatting. (e.g., "너는 누구야?", "안녕")

Second, based on the intent, provide one of the following:
- If the intent is `specific_search`, extract the exact keyword (artist or song title). The keyword should be in English if it's a well-known artist.
- If the intent is `exploratory_recommendation`, create a descriptive and effective search query in Korean to find a single "seed song" that matches the user's request for Korean music.

Return the result as a single, minified JSON object.

Example 1 (Specific Search):
User Message: "아이유 노래 추천해줘"
Result: {{"intent": "specific_search", "keyword": "IU"}}

Example 2 (Exploratory Recommendation):
User Message: "비 오는 날 듣기 좋은 잔잔한 노래 찾아줘"
Result: {{"intent": "exploratory_recommendation", "query": "비 오는 날 잔잔한 한국 노래"}}

Example 3 (Specific Search):
User Message: "방탄소년단 버터 좀 찾아줘"
Result: {{"intent": "specific_search", "keyword": "BTS Butter"}}

Example 4 (General Conversation):
User Message: "오늘 날씨 어때?"
Result: {{"intent": "general_conversation", "keyword": null, "query": null}}
"""
    try:
        response_content = llm.invoke([HumanMessage(content=prompt)]).content
        if response_content.startswith("```json") and response_content.endswith("```"):
            response_content = response_content[7:-3].strip()
        return json.loads(response_content)
    except Exception as e:
        print(f"[오류] LLM 의도 분석 중 문제 발생: {e}")
        return {{"intent": "error"}}


def search_specific_music(sp_client, keyword, limit=5):
    """
    특정 키워드(아티스트, 곡명)로 직접 검색을 수행합니다.
    """
    try:
        print(f"[정보] 특정 검색 실행. 키워드: '{keyword}', 마켓: KR")
        results = sp_client.search(q=keyword, type='track', limit=limit, market='KR')
        if not results['tracks']['items']:
            return None
        
        tracks = []
        for track in results['tracks']['items']:
            tracks.append({
                'name': track['name'],
                'artist': ', '.join([a['name'] for a in track['artists']]),
                'url': track['external_urls']['spotify'],
                'album_image_url': track['album']['images'][0]['url'] if track['album']['images'] else None,
                'id': track['id'] # Spotify ID 추가
            })
        return tracks
    except Exception as e:
        print(f"[오류] 특정 검색 중 오류 발생: {e}")
        return None


def get_recommendations_via_expanded_search(sp_client, initial_query, limit=5):
    """
    한국인 아티스트 검증 및 장르 확장 검색으로 탐색적 추천을 수행합니다.
    """
    try:
        print(f"[정보] 탐색적 추천 1단계: 시드 후보 검색. 쿼리: '{initial_query}', 마켓: KR")
        search_result = sp_client.search(q=initial_query, type='track', limit=10, market='KR')

        if not search_result['tracks']['items']:
            return search_music_fallback(sp_client, initial_query, limit)

        seed_artist_id = None
        seed_artist_name = ""
        seed_artist_genres = []

        for track in search_result['tracks']['items']:
            artist_id = track['artists'][0]['id']
            artist_info = sp_client.artist(artist_id)
            genres = artist_info.get('genres', [])
            is_korean_artist = any('k-pop' in g or 'korean' in g for g in genres)
            
            if is_korean_artist:
                seed_artist_id = artist_id
                seed_artist_name = artist_info['name']
                seed_artist_genres = genres
                print(f"[정보] 탐색적 추천 2단계: 한국인 시드 아티스트 '{seed_artist_name}' 발견.")
                break
        
        if not seed_artist_id:
            return search_music_fallback(sp_client, initial_query, limit)

        if not seed_artist_genres:
            return search_music_fallback(sp_client, f"artist:{seed_artist_name}", limit)

        genre_query = ' '.join([f'genre:"{g}"' for g in seed_artist_genres[:3]])
        print(f"[정보] 탐색적 추천 3단계: 확장 검색 실행. 쿼리: '{genre_query}', 마켓: KR")
        final_results = sp_client.search(q=genre_query, type='track', limit=limit, market='KR')

        if not final_results['tracks']['items']:
            return search_music_fallback(sp_client, initial_query, limit)

        recommended_tracks = []
        for track in final_results['tracks']['items']:
            recommended_tracks.append({
                'name': track['name'],
                'artist': ', '.join([a['name'] for a in track['artists']]),
                'url': track['external_urls']['spotify'],
                'album_image_url': track['album']['images'][0]['url'] if track['album']['images'] else None,
                'id': track['id'] # Spotify ID 추가
            })
        return recommended_tracks

    except Exception as e:
        print(f"[오류] 확장 검색 중 오류 발생: {e}")
        return search_music_fallback(sp_client, initial_query, limit)


def search_music_fallback(sp_client, query, limit=5):
    """확장 검색 실패 시 사용될 단순 검색 기능"""
    print(f"[정보] 폴백(단순) 검색 실행. 쿼리: '{query}', 마켓: KR")
    return search_specific_music(sp_client, query, limit)


def _get_llm_response(chat_history, user_input):
    messages = [AIMessage(content="You are a helpful assistant.")] + [HumanMessage(content=msg[4:].strip()) if msg.startswith("당신:") else AIMessage(content=msg[4:].strip()) for msg in chat_history] + [HumanMessage(content=user_input)]
    try:
        return llm.invoke(messages).content
    except Exception as e:
        print(f"[오류] LLM 응답 생성 중 문제 발생: {e}")
        return "죄송합니다. 지금은 답변을 드릴 수 없습니다."
