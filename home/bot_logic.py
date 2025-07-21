import json
import spotipy
from langchain_openai import ChatOpenAI
from django.conf import settings
from home.lastfm_utils import get_similar_tracks_by_artist, get_tracks_by_tags
from home.mapping import MOOD_TAG_MAPPING as MOOD_TRANSLATION_MAP, GENRE_TAG_MAPPING

# LLM 초기화
llm = ChatOpenAI(
    model="gpt-3.5-turbo",
    api_key=settings.OPENAI_API_KEY
)

def analyze_user_intent(user_message):
    prompt = f"""너는 사용자의 음악 추천 요청을 분석해서 intent와 keyword를 JSON으로 반환하는 분석기야.
사용자가 \"{user_message}\"라고 입력했어.

'keywords'는 1개 이상이야. 단, '노래', '음악', '추천'처럼 일반적인 단어는 포함하지 마.
감정(예: 슬픈), 장르(예: 케이팝), 분위기/스타일(예: 차분한) 등 **의미 있는 키워드**만 포함시켜.

※ 주의: 사용자가 직접 언급하지 않은 지역/언어(예: 한국) 키워드는 넣지 마.

다음 형식의 JSON으로 응답해:
{{
  "intent": "recommend_by_mood",  // 또는 "recommend_by_genre", "recommend_by_keyword", "search_music", "etc"
  "keywords": ["슬픈"]            // 꼭 여러 개 넣되, 일반 단어는 제외하고 사용자 의도에 맞는 의미 있는 키워드만 포함!
}}
"""



    try:
        response_content = _get_llm_response(prompt)
        print("LLM 응답:", response_content)
        if response_content.startswith("```json"):
            response_content = response_content[7:-3].strip()
        return json.loads(response_content)
    except Exception as e:
        print(f"[오류] LLM 의도 분석 중 문제 발생: {e}")
        return {"intent": "error"}

def normalize_keywords(keywords):
    mood_tag = None
    genre_tag = None

    for keyword in keywords:
        k = keyword.strip()

        # 정확히 일치
        if k in MOOD_TRANSLATION_MAP:
            mood_tag = MOOD_TRANSLATION_MAP[k]
        elif k in GENRE_TAG_MAPPING:
            genre_tag = GENRE_TAG_MAPPING[k]
        else:
            # 포함된 경우 대응
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