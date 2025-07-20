import os
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

class Command(BaseCommand):
    help = 'Tests Spotify API integration by searching for a track.'

    def handle(self, *args, **options):
        client_id = settings.SPOTIPY_CLIENT_ID
        client_secret = settings.SPOTIPY_CLIENT_SECRET

        if not client_id or not client_secret:
            raise CommandError("Spotify Client ID or Client Secret is not set in settings.py")

        try:
            sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=client_id, client_secret=client_secret))
            
            # Search for a popular track to test
            results = sp.search(q='track:Dynamite artist:BTS', type='track', limit=1)

            if results and results['tracks']['items']:
                track = results['tracks']['items'][0]
                self.stdout.write(self.style.SUCCESS(f"Successfully connected to Spotify API!"))
                self.stdout.write(self.style.SUCCESS(f"Found track: {track['name']} by {track['artists'][0]['name']}"))
                self.stdout.write(self.style.SUCCESS(f"Preview URL: {track['preview_url']}"))
            else:
                self.stdout.write(self.style.WARNING("Successfully connected to Spotify API, but no track found for 'Dynamite by BTS'."))

        except Exception as e:
            raise CommandError(f"Error connecting to Spotify API: {e}")