import os
from django.core.management.base import BaseCommand
from django.conf import settings
from mypage.models import Track
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

class Command(BaseCommand):
    help = 'Updates track information (image_url, title, artist) from Spotify API.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Updating track information...'))

        sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
            client_id=settings.SPOTIPY_CLIENT_ID,
            client_secret=settings.SPOTIPY_CLIENT_SECRET
        ))

        tracks_to_update = Track.objects.filter(spotify_id__isnull=False).exclude(image_url__isnull=False, title__isnull=False, artist__isnull=False)

        if not tracks_to_update.exists():
            self.stdout.write(self.style.SUCCESS('No tracks to update.'))
            return

        for track in tracks_to_update:
            try:
                spotify_track = sp.track(track.spotify_id)
                updated = False

                if not track.image_url and spotify_track['album']['images']:
                    track.image_url = spotify_track['album']['images'][0]['url']
                    updated = True
                
                # Track 모델의 name 필드가 아닌 title 필드를 사용하므로, title을 업데이트
                if not track.title and spotify_track['name']:
                    track.title = spotify_track['name']
                    updated = True

                if not track.artist and spotify_track['artists']:
                    track.artist = spotify_track['artists'][0]['name']
                    updated = True

                if updated:
                    track.save()
                    self.stdout.write(self.style.SUCCESS(f'Successfully updated track: {track.title} - {track.artist}'))
                else:
                    self.stdout.write(self.style.WARNING(f'No updates needed for track: {track.title} - {track.artist}'))

            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error updating track {track.spotify_id}: {e}'))

        self.stdout.write(self.style.SUCCESS('Track information update complete.'))
