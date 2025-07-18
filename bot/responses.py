import random
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage
import os
from dotenv import load_dotenv
# OpenAI 모델 초기화 (환경 변수 OPENAI_API_KEY 필요)
# 가장 저렴한 모델 중 하나인 gpt-3.5-turbo를 사용합니다.
load_dotenv()
llm = ChatOpenAI(
    model="gpt-3.5-turbo",
    api_key = os.getenv("OPENAI_API_KEY")    
    )

def _get_llm_response(chat_history, user_input):
    """
    대규모 언어 모델(LLM)을 사용하여 응답을 생성합니다.

    Args:
        chat_history (list): 이전 대화 기록 (예: ["당신: 안녕하세요", "챗봇: 안녕하세요!"])
        user_input (str): 현재 사용자의 입력

    Returns:
        str: LLM이 생성한 응답
    """
    messages = []
    # 이전 대화 기록을 LangChain 메시지 형식으로 변환
    for msg in chat_history:
        if msg.startswith("당신:"):
            messages.append(HumanMessage(content=msg[4:].strip()))
        elif msg.startswith("챗봇:"):
            messages.append(AIMessage(content=msg[4:].strip()))
    
    # 현재 사용자 입력을 추가
    messages.append(HumanMessage(content=user_input))

    try:
        response = llm.invoke(messages).content
        return response
    except Exception as e:
        print(f"[오류] LLM 응답 생성 중 문제 발생: {e}")
        return "죄송합니다. 지금은 답변을 드릴 수 없습니다."

def get_response(user_input, conversation_state):
    """
    사용자 입력과 현재 대화 상태에 따라 적절한 응답을 반환하고 대화 상태를 업데이트합니다.
    이전 대화 기록을 활용하여 맥락을 파악합니다.

    Args:
        user_input (str): 사용자가 입력한 문자열
        conversation_state (dict): 현재 대화의 상태를 담고 있는 딕셔너리.
                                   'chat_history' (list): 이전 대화 기록 (사용자 입력, 챗봇 응답 순)
                                   'stage': 현재 대화의 단계 (initial, asking_name 등)

    Returns:
        tuple: (챗봇의 응답 메시지, 업데이트된 대화 상태)
    """
    lowered_input = user_input.lower()
    response = ""

    # 대화 기록에 현재 사용자 입력 추가
    conversation_state.setdefault('chat_history', []).append(f"당신: {user_input}")

    # 대화 단계 초기화 (새로운 대화 시작 또는 이전 대화가 종료된 경우)
    if 'stage' not in conversation_state:
        conversation_state['stage'] = 'initial'

    # 종료 키워드 처리 (chatbot.py에서 최종 종료)
    if "잘가" in lowered_input or "안녕히" in lowered_input or "종료" in lowered_input:
        response = random.choice(["다음에 또 만나요!", "안녕히 가세요!", "즐거운 하루 되세요!"])
        conversation_state['stage'] = 'exit' # 종료 단계로 설정
    else:
        # LLM을 통해 응답 생성
        response = _get_llm_response(conversation_state['chat_history'], user_input)
        conversation_state['stage'] = 'initial' # 응답 후 초기 상태로

    # 챗봇 응답을 대화 기록에 추가
    conversation_state['chat_history'].append(f"챗봇: {response}")

    return response, conversation_state
