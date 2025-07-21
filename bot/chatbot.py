import responses
import datetime

def save_chat_history(user_input, bot_response):
    """
    대화 내용을 파일에 저장합니다.

    Args:
        user_input (str): 사용자의 입력
        bot_response (str): 챗봇의 응답
    """
    # 현재 시간을 YYYY-MM-DD HH:MM:SS 형식으로 기록합니다.
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        # chat_history.log 파일을 추가 모드(a)로 열어 대화 내용을 기록합니다.
        with open("chat_history.log", "a", encoding="utf-8") as f:
            f.write(f"[{timestamp}] 당신: {user_input}\n")
            f.write(f"[{timestamp}] 챗봇: {bot_response}\n")
    except Exception as e:
        print(f"[오류] 대화 기록 저장 중 문제가 발생했습니다: {e}")


def start_chat():
    """
    챗봇과의 대화를 시작하는 함수입니다.
    """
    print("안녕하세요! 챗봇입니다. 무엇을 도와드릴까요? (종료하려면 '종료' 또는 '잘가'를 입력하세요)")

    # 대화 상태 초기화
    conversation_state = {
        'stage': 'initial',
        'chat_history': [] # 이전 대화 기록을 저장할 리스트
    }

    while True:
        try:
            user_input = input("당신: ")

            # 1. 입력 검증: 사용자가 아무것도 입력하지 않은 경우
            if not user_input.strip():
                print("챗봇: 아무 말씀도 안 하셨네요. 다시 한번 말씀해주시겠어요?")
                continue

            # get_response 함수에 conversation_state 전달 및 업데이트
            response, conversation_state = responses.get_response(user_input, conversation_state)
            print(f"챗봇: {response}")

            # responses.py에서 'exit' 단계로 설정된 경우 대화 종료
            if conversation_state['stage'] == 'exit':
                break

            # 2. 대화 기록 저장
            save_chat_history(user_input, response)

        except (KeyboardInterrupt, EOFError):
            print("\n챗봇: 대화를 종료합니다. 안녕히 가세요!")
            break
        # 3. 포괄적인 오류 처리
        except Exception as e:
            print(f"[오류] 예상치 못한 문제가 발생했습니다: {e}")
            save_chat_history(user_input, f"[오류 발생] {e}")
            break

def main():
    """
    챗봇 프로그램을 실행하는 메인 함수입니다.
    """
    start_chat()

if __name__ == "__main__":
    main()