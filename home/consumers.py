import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.conf import settings
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from asgiref.sync import sync_to_async
# bot_logic.py에서 함수 임포트 
# ✅ 수정된 코드
from .bot_logic import normalize_keywords

from .bot_logic import analyze_user_intent, search_specific_music, get_recommendations_via_expanded_search, _get_llm_response

class HomeChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = 'home_chat_room'
        self.room_group_name = 'home_chat_%s' % self.room_name

        # Initialize Spotify client
        import requests
        session = requests.Session()
        session.headers.update({'Accept-Language': 'ko-KR'})
        self.spotify = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
            client_id=settings.SPOTIPY_CLIENT_ID,
            client_secret=settings.SPOTIPY_CLIENT_SECRET
        ), requests_session=session)

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        user_message = text_data_json.get('message', '')
        if not user_message:
            return

        print(f"Received message from user on home chat: {user_message}")

        # 챗봇 로직 통합 시작
        intent_data = await sync_to_async(analyze_user_intent)(user_message)
        intent = intent_data.get("intent")
        tracks = None
        bot_response = ""
        recommended_tracks = []

        if intent == 'specific_search':
            keyword = intent_data.get('keyword')
            if keyword:
                tracks = await sync_to_async(search_specific_music)(self.spotify, keyword)
                if tracks:
                    bot_response = "이런 음악은 어떠세요? 마음에 드셨으면 좋겠네요!"
                    recommended_tracks = tracks
                else:
                    bot_response = "죄송합니다. 요청하신 음악을 찾지 못했어요. 다른 표현으로 말씀해주시겠어요?"
            else:
                bot_response = "어떤 곡이나 아티스트를 찾으시는지 더 자세히 알려주세요."
        elif intent == 'exploratory_recommendation':
            query = intent_data.get('query')
            if query:
                tracks = await sync_to_async(get_recommendations_via_expanded_search)(self.spotify, query)
                if tracks:
                    bot_response = "이런 음악은 어떠세요? 마음에 드셨으면 좋겠네요!"
                    recommended_tracks = tracks
                else:
                    bot_response = "죄송합니다. 요청하신 분위기에 맞는 음악을 찾지 못했어요. 다른 표현으로 말씀해주시겠어요?"
            else:
                bot_response = "어떤 분위기의 음악을 찾으시는지 더 자세히 알려주세요."
        elif intent == 'recommend_by_keyword':
            keyword = intent_data.get('keyword')
            if keyword:
                from .bot_logic import normalize_keyword  # 추가해줘야 해
                normalized = normalize_keyword(keyword)   # ✅ 여기서 변환
                tracks = await sync_to_async(search_specific_music)(self.spotify, normalized)
                if tracks:
                    bot_response = f"'{keyword}' 관련 음악을 추천드릴게요!"
                    recommended_tracks = tracks
                else:
                    bot_response = f"'{keyword}'와 관련된 음악을 찾지 못했어요."
            else:
                bot_response = "추천을 원하시는 음악 키워드를 입력해주세요."
        elif intent == 'recommend_by_mood':
            from .bot_logic import normalize_keywords
            keywords = intent_data.get('keywords', [])
            mood_tag, genre_tag = normalize_keywords(keywords)

            if mood_tag or genre_tag:
                from .lastfm_utils import get_tracks_by_tags
                tracks = await sync_to_async(get_tracks_by_tags)(mood_tag, genre_tag)
                if tracks:
                    bot_response = f"{', '.join(keywords)} 분위기의 음악을 추천드릴게요!"
                    recommended_tracks = tracks
                else:
                    bot_response = f"{', '.join(keywords)} 분위기에 맞는 음악을 찾지 못했어요."
            else:
                bot_response = f"'{', '.join(keywords)}'에서 추천 가능한 분위기를 찾지 못했어요."
        elif intent == 'recommend_by_genre':
            from .bot_logic import normalize_keywords
            keywords = intent_data.get('keywords', [])
            mood_tag, genre_tag = normalize_keywords(keywords)

            if genre_tag or mood_tag:
                from .lastfm_utils import get_tracks_by_tags
                tracks = await sync_to_async(get_tracks_by_tags)(mood_tag, genre_tag)
                if tracks:
                    bot_response = f"{', '.join(keywords)} 장르의 음악을 추천드릴게요!"
                    recommended_tracks = tracks
                else:
                    bot_response = f"{', '.join(keywords)} 장르에 맞는 음악을 찾지 못했어요."
            else:
                bot_response = f"'{', '.join(keywords)}'에서 추천 가능한 장르를 찾지 못했어요."
        elif intent == 'recommend_by_weather':
            city = intent_data.get('city')
            from .bot_logic import recommend_by_current_weather
            bot_response, recommended_tracks = await sync_to_async(recommend_by_current_weather)(city)


    
        elif intent == 'general_conversation':
            bot_response = await sync_to_async(_get_llm_response)([], user_message)
        else:
            bot_response = "죄송합니다. 이해하지 못했습니다. 다시 말씀해주시겠어요."

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'home_chat_message',
                'sender': 'bot',
                'message': bot_response,
                'recommendations': recommended_tracks
            }
        )

    async def home_chat_message(self, event):
        message = event['message']
        sender = event.get('sender', 'bot')
        recommendations = event.get('recommendations', [])

        await self.send(text_data=json.dumps({
            'message': message,
            'sender': sender,
            'recommendations': recommendations
        }))