import random
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage
import os
from dotenv import load_dotenv
from utils import get_weather
import json
from home.bot_logic import get_recommendations_by_weather_tags, normalize_weather_description_with_llm

# OpenAI 모델 초기화
load_dotenv()
llm = ChatOpenAI(
    model="gpt-3.5-turbo",
    api_key=os.getenv("OPENAI_API_KEY")
)

def _get_llm_response(chat_history, user_input):
    """
    대규모 언어 모델(LLM)을 사용하여 일반 대화 응답을 생성합니다.
    """
    messages = []
    for msg in chat_history:
        if msg.startswith("당신:"):
            messages.append(HumanMessage(content=msg[4:].strip()))
        elif msg.startswith("챗봇:"):
            messages.append(AIMessage(content=msg[4:].strip()))
    
    messages.append(HumanMessage(content=user_input))

    try:
        return llm.invoke(messages).content
    except Exception as e:
        print(f"[오류] LLM 응답 생성 중 문제 발생: {e}")
        return "죄송합니다. 지금은 답변을 드릴 수 없습니다."

def _get_user_intent(user_input):
    """
    LLM을 사용하여 사용자의 의도와 도시 정보를 분석하고 JSON 형식으로 반환합니다.
    """
    prompt = f"""사용자의 다음 메시지에서 의도(intent)와 도시(city)를 분석해주세요.

    의도는 다음 세 가지 중 하나로 분류해주세요:
    1. GET_WEATHER: 사용자가 특정 지역의 날씨를 직접적으로 물어볼 때.
    2. RECOMMEND_SONG_BASED_ON_WEATHER: 사용자가 날씨와 관련된 노래 추천을 원할 때.
    3. GENERAL_CONVERSATION: 위 두 가지에 해당하지 않는 모든 일반적인 대화.

    도시(city)는 문장에서 언급된 경우에만 추출하고, 없으면 null로 설정해주세요.
    응답은 반드시 JSON 형식으로만 반환해주세요. 예: {{"intent": "GET_WEATHER", "city": "서울"}}

    사용자 메시지: "{user_input}"
    """
    
    try:
        response = llm.invoke([HumanMessage(content=prompt)]).content
        # LLM 응답이 JSON 형식이 아닐 경우를 대비한 예외 처리
        intent_data = json.loads(response)
        # city가 없을 경우 None으로 통일
        intent_data['city'] = intent_data.get('city') 
        return intent_data
    except (json.JSONDecodeError, KeyError) as e:
        print(f"[오류] 의도 분석 실패 (LLM 응답: {response}): {e}")
        # 분석 실패 시 일반 대화로 처리
        return {"intent": "GENERAL_CONVERSATION", "city": None}
    except Exception as e:
        print(f"[오류] 의도 분석 중 예외 발생: {e}")
        return {"intent": "GENERAL_CONVERSATION", "city": None}

def get_response(user_input, conversation_state):
    """
    사용자 입력의 의도를 파악하여 적절한 응답을 반환하고 대화 상태를 업데이트합니다.
    """
    lowered_input = user_input.lower().strip()
    response = ""

    conversation_state.setdefault('chat_history', []).append(f"당신: {user_input}")
    if 'stage' not in conversation_state:
        conversation_state['stage'] = 'initial'

    # --- 상태 기반 응답 처리 (도시를 물어본 후) ---
    if conversation_state.get('stage') == 'awaiting_city_for_recommendation':
        city = user_input.strip()
        weather_info = get_weather(city=city)
        if "오류" in weather_info or "없습니다" in weather_info:
            response = weather_info
        else:
            # 날씨 기반 태그 추천 함수 호출
            normalized_weather = normalize_weather_description_with_llm(weather_info)
            recommended_tracks, used_mood_tag, used_genre_tag = get_recommendations_by_weather_tags(normalized_weather)
            if recommended_tracks:
                response = f"{city}의 날씨는 '{weather_info}'입니다.\n"
                response += f"매핑된 날씨 태그: {normalized_weather} -> {used_mood_tag}, {used_genre_tag}\n"
                response += f"이 날씨에 어울리는 곡을 추천해 드릴게요:\n"
                for track in recommended_tracks:
                    response += f"- {track['name']} - {track['artist']}\n"
                response += f"추천에 사용된 태그: 기분={used_mood_tag}, 장르={used_genre_tag}"
            else:
                response = f"{city}의 날씨는 '{weather_info}'입니다. 죄송하지만, 이 날씨에 맞는 곡을 찾을 수 없네요."
        conversation_state['stage'] = 'initial'

    elif conversation_state.get('stage') == 'asking_for_city':
        city = user_input.strip()
        response = get_weather(city=city)
        conversation_state['stage'] = 'initial'

    # --- 의도 분석 기반 응답 처리 ---
    else:
        intent_data = _get_user_intent(user_input)
        intent = intent_data.get("intent")
        city = intent_data.get("city")

        # 1. 날씨 기반 노래 추천 의도
        if intent == "RECOMMEND_SONG_BASED_ON_WEATHER":
            if city:
                weather_info = get_weather(city=city)
                if "오류" in weather_info or "없습니다" in weather_info:
                    response = weather_info
                else:
                    # 날씨 기반 태그 추천 함수 호출
                    normalized_weather = normalize_weather_description_with_llm(weather_info)
                    recommended_tracks, used_mood_tag, used_genre_tag = get_recommendations_by_weather_tags(normalized_weather)
                    if recommended_tracks:
                        response = f"{city}의 날씨는 '{weather_info}'입니다.\n"
                        response += f"매핑된 날씨 태그: {normalized_weather} -> {used_mood_tag}, {used_genre_tag}\n"
                        response += f"이 날씨에 어울리는 곡을 추천해 드릴게요:\n"
                        for track in recommended_tracks:
                            response += f"- {track['name']} - {track['artist']}\n"
                        response += f"추천에 사용된 태그: 기분={used_mood_tag}, 장르={used_genre_tag}"
                    else:
                        response = f"{city}의 날씨는 '{weather_info}'입니다. 죄송하지만, 이 날씨에 맞는 곡을 찾을 수 없네요."
                conversation_state['stage'] = 'initial'
            else:
                response = "어느 도시의 날씨를 기반으로 추천해 드릴까요?"
                conversation_state['stage'] = 'awaiting_city_for_recommendation'

        # 2. 단순 날씨 조회 의도
        elif intent == "GET_WEATHER":
            if city:
                response = get_weather(city=city)
            else:
                response = "어느 도시의 날씨가 궁금하신가요?"
                conversation_state['stage'] = 'asking_for_city'
        
        # 3. 일반 대화 또는 종료
        else: # GENERAL_CONVERSATION
            if "잘가" in lowered_input or "안녕히" in lowered_input or "종료" in lowered_input:
                response = random.choice(["다음에 또 만나요!", "안녕히 가세요!", "즐거운 하루 되세요!"])
                conversation_state['stage'] = 'exit'
            else:
                response = _get_llm_response(conversation_state['chat_history'], user_input)
                conversation_state['stage'] = 'initial'

    # 챗봇 응답을 대화 기록에 추가
    if response:
        conversation_state['chat_history'].append(f"챗봇: {response}")

    return response, conversation_state