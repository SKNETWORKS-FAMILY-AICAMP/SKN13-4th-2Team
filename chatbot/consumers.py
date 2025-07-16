import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.conf import settings
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from asgiref.sync import sync_to_async

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
        user_message = text_data_json['message']
        print(f"Received message from user: {user_message}")

        # Send user message to room group (for display in chat log)
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'sender': 'user',
                'message': user_message
            }
        )

        # Simple recommendation logic: search Spotify for tracks
        try:
            results = await sync_to_async(self.spotify.search)(
                q=user_message, type='track', limit=3
            )
            
            recommended_tracks = []
            if results and results['tracks']['items']:
                for track in results['tracks']['items']:
                    recommended_tracks.append({
                        'name': track['name'],
                        'artist': track['artists'][0]['name'] if track['artists'] else 'Unknown Artist',
                        'url': track['external_urls']['spotify']
                    })
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
        print(f"Received message from channel layer for sender {sender}: {message}")

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'sender': sender,
            'recommendations': recommendations
        }))
        print(f"Message sent to WebSocket for sender {sender}.")