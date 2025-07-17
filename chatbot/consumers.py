import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.conf import settings
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from asgiref.sync import sync_to_async
from mypage.models import Playlist, Track # Import Playlist and Track models

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = 'chatbot_room' # You can make this dynamic if needed
        self.room_group_name = 'chat_%s' % self.room_name

        # Initialize Spotify client
        self.spotify = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
            client_id=settings.SPOTIPY_CLIENT_ID,
            client_secret=settings.SPOTIPY_CLIENT_SECRET
        ))

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message_type = text_data_json.get('type') # 메시지 타입을 가져옵니다.

        if message_type == 'create_playlist_request':
            playlist_name = text_data_json.get('playlist_name', 'New Playlist')
            selected_tracks_data = text_data_json.get('tracks', [])
            user = self.scope["user"] # Get the current user

            if not user.is_authenticated:
                await self.send(text_data=json.dumps({
                    'message': '플레이리스트를 생성하려면 로그인해야 합니다.',
                    'sender': 'bot'
                }))
                return

            print(f"[Playlist Creation] Received playlist_name: {playlist_name}")
            print(f"[Playlist Creation] Received selected_tracks_data: {selected_tracks_data}")

            try:
                # Create the playlist in a synchronous context
                new_playlist = await sync_to_async(Playlist.objects.create)(
                    user=user,
                    name=playlist_name,
                    description="Created from chatbot recommendations"
                )
                print(f"[Playlist Creation] New playlist created with ID: {new_playlist.id}")

                track_objects = []
                for track_data in selected_tracks_data:
                    # Find or create Track objects in a synchronous context
                    track, created = await sync_to_async(Track.objects.get_or_create)(
                        spotify_id=track_data['id'],
                        defaults={
                            'title': track_data['name'],
                            'artist': track_data['artist']
                        }
                    )
                    track_objects.append(track)
                    print(f"[Playlist Creation] Processed track: {track.title} (Created: {created})")

                print(f"[Playlist Creation] Final track_objects to add: {track_objects}")
                # Add tracks to the playlist in a synchronous context
                await sync_to_async(new_playlist.tracks.add)(*track_objects)
                print(f"[Playlist Creation] Added {len(track_objects)} tracks to playlist {new_playlist.id}.")

                await self.send(text_data=json.dumps({
                    'message': f"'{playlist_name}' 플레이리스트가 성공적으로 생성되었습니다!",
                    'sender': 'bot'
                }))
                print(f"Playlist '{playlist_name}' created for user {user.username} with {len(track_objects)} tracks.")

            except Exception as e:
                print(f"Error creating playlist: {e}")
                await self.send(text_data=json.dumps({
                    'message': f"플레이리스트 생성 중 오류가 발생했습니다: {e}",
                    'sender': 'bot'
                }))

        else:
            # 기존 챗봇 메시지 처리 로직
            user_message = text_data_json.get('message', '') # 안전하게 .get() 사용
            if not user_message: # 빈 메시지 처리
                return

            print(f"Received message from user: {user_message}")

            # Simple recommendation logic: search Spotify for tracks
            print("Attempting Spotify search...")
            try:
                results = await sync_to_async(self.spotify.search)(
                    q=user_message, type='track', limit=10
                )
                print(f"Spotify search results received. Number of items: {len(results['tracks']['items']) if results and results['tracks'] else 0}")

                recommended_tracks = []
                seen_track_ids = set() # Add this line to keep track of seen Spotify IDs

                if results and results['tracks']['items']:
                    for track in results['tracks']['items']:
                        track_id = track['id'] # Get Spotify track ID

                        if track_id not in seen_track_ids: # Check for duplicates
                            seen_track_ids.add(track_id) # Add to seen set

                            album_image_url = None
                            if track['album'] and track['album']['images']:
                                # Get the URL of the first (usually largest) album image
                                album_image_url = track['album']['images'][0]['url']

                            recommended_tracks.append({
                                'id': track['id'], # 이 줄을 추가합니다.
                                'name': track['name'],
                                'artist': track['artists'][0]['name'] if track['artists'] else 'Unknown Artist',
                                'url': track['external_urls']['spotify'],
                                'album_image_url': album_image_url # Add this line
                            })
                    print(f"Deduplicated recommended_tracks: {recommended_tracks}")
                    bot_response = "Here are some tracks I found for you:"
                    print(f"Spotify search successful. Found {len(recommended_tracks)} tracks.")
                else:
                    bot_response = "Sorry, I couldn't find any tracks for that. Can you try something else?"
                    print("Spotify search found no tracks.")

            except Exception as e:
                bot_response = f"An error occurred while searching for music: {e}"
                recommended_tracks = []
                print(f"Spotify API Error: {e}")

            print(f"Bot response generated: {bot_response}")
            print(f"Sending to channel layer. Recommendations count: {len(recommended_tracks)}")
            # Send bot response and recommendations to room group
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'sender': 'bot',
                    'message': bot_response,
                    'recommendations': recommended_tracks
                }
            )
            print("Bot response sent to channel layer.")

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        sender = event.get('sender', 'bot')
        recommendations = event.get('recommendations', [])
        print(f"[chat_message] Received from channel layer. Sender: {sender}, Message: {message[:50]}..., Recommendations count: {len(recommendations)}")

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'sender': sender,
            'recommendations': recommendations
        }))
        print(f"[chat_message] Message sent to WebSocket for sender {sender}. Recommendations count: {len(recommendations)}")