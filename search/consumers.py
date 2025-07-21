import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.conf import settings
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from asgiref.sync import sync_to_async
from mypage.models import Playlist, Track

class SearchConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = 'search_room'
        self.room_group_name = 'search_%s' % self.room_name

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
        message_type = text_data_json.get('type')
        source = text_data_json.get('source', 'user_query')
        search_type = text_data_json.get('search_type', 'track')

        if message_type == 'create_playlist_request':
            playlist_name = text_data_json.get('playlist_name', '새 플레이리스트')
            selected_tracks_data = text_data_json.get('tracks', [])
            user = self.scope["user"]

            if not user.is_authenticated:
                await self.send(text_data=json.dumps({
                    'message': '플레이리스트를 생성하려면 로그인해야 합니다.',
                    'sender': 'bot'
                }))
                return

            try:
                new_playlist = await sync_to_async(Playlist.objects.create)(
                    user=user,
                    name=playlist_name,
                    description="챗봇 추천으로 생성됨"
                )
                track_objects = []
                for track_data in selected_tracks_data:
                    track, created = await sync_to_async(Track.objects.get_or_create)(
                        spotify_id=track_data['id'],
                        defaults={
                            'title': track_data['name'],
                            'artist': track_data['artist']
                        }
                    )
                    track_objects.append(track)
                await sync_to_async(new_playlist.tracks.add)(*track_objects)
                await self.send(text_data=json.dumps({
                    'message': f"'{playlist_name}' 플레이리스트가 성공적으로 생성되었습니다!",
                    'sender': 'bot'
                }))
            except Exception as e:
                await self.send(text_data=json.dumps({
                    'message': f"플레이리스트 생성 중 오류가 발생했습니다: {e}",
                    'sender': 'bot'
                }))

        else:
            user_message = text_data_json.get('message', '')
            if not user_message:
                return

            try:
                results = await sync_to_async(self.spotify.search)(
                    q=user_message, type=search_type, limit=10
                )
                recommended_tracks = []
                seen_track_ids = set()
                items = results.get(f'{search_type}s', {}).get('items', [])

                for item in items:
                    if search_type == 'track':
                        track_id = item['id']
                        if track_id not in seen_track_ids:
                            seen_track_ids.add(track_id)
                            album_image_url = item['album']['images'][0]['url'] if item['album']['images'] else None
                            recommended_tracks.append({
                                'id': item['id'],
                                'name': item['name'],
                                'artist': item['artists'][0]['name'] if item['artists'] else '알 수 없음',
                                'url': item['external_urls']['spotify'],
                                'album_image_url': album_image_url
                            })
                    elif search_type == 'artist':
                        recommended_tracks.append({
                            'id': item['id'],
                            'name': item['name'],
                            'artist': '',  # 아티스트명 없음
                            'url': item['external_urls']['spotify'],
                            'album_image_url': (item['images'][0]['url'] if item.get('images') else None)
                        })
                    elif search_type == 'album':
                        recommended_tracks.append({
                            'id': item['id'],
                            'name': item['name'],
                            'artist': item['artists'][0]['name'] if item['artists'] else '',
                            'url': item['external_urls']['spotify'],
                            'album_image_url': (item['images'][0]['url'] if item.get('images') else None)
                        })

                type_for_front = search_type  # 프론트에 내려줌

                if source == 'user_query':
                    bot_response = "아래 추천곡을 찾아왔어요!"
                else:
                    bot_response = ""

                if not recommended_tracks:
                    bot_response = "해당 검색어로 곡을 찾지 못했습니다. 다른 검색어로 시도해보세요."

            except Exception as e:
                bot_response = f"음악을 검색하는 중 오류가 발생했습니다: {e}"
                recommended_tracks = []
                type_for_front = 'track'

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'search_message',
                    'sender': 'bot',
                    'message': bot_response,
                    'recommendations': recommended_tracks,
                    'search_type': type_for_front  # type 정보 추가!
                }
            )

    async def search_message(self, event):
        message = event['message']
        sender = event.get('sender', 'bot')
        recommendations = event.get('recommendations', [])
        search_type = event.get('search_type', 'track')  # 프론트로 전달

        await self.send(text_data=json.dumps({
            'message': message,
            'sender': sender,
            'recommendations': recommendations,
            'search_type': search_type
        }))
