from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages # Import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import json
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from django.conf import settings

from .models import Profile, Playlist, ListeningHistory, Track
from .forms import ProfileForm, PlaylistForm

import requests

# Initialize Spotify client (similar to chatbot consumer)
session = requests.Session()
session.headers.update({'Accept-Language': 'ko-KR'})
spotify_client = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id=settings.SPOTIPY_CLIENT_ID,
    client_secret=settings.SPOTIPY_CLIENT_SECRET
), requests_session=session)

@login_required
def index(request):
    user_profile = request.user.profile
    playlists = Playlist.objects.filter(user=request.user).order_by('-created_at')
    # Calculate track count for each playlist
    for playlist in playlists:
        playlist.track_count = playlist.tracks.count() # Explicitly get the count
    return render(request, 'mypage/index.html', {'user_profile': user_profile, 'playlists': playlists})

@login_required
def profile_edit(request):
    user_profile = request.user.profile
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            messages.success(request, "프로필이 성공적으로 업데이트되었습니다.") # Add success message
            return redirect('mypage:index')
    else:
        form = ProfileForm(instance=user_profile)
    return render(request, 'mypage/profile_edit.html', {'form': form})

@login_required
def create_playlist(request):
    form = PlaylistForm()
    selected_tracks_data = []

    if request.method == 'POST':
        form = PlaylistForm(request.POST)
        if form.is_valid():
            playlist = form.save(commit=False)
            playlist.user = request.user
            playlist.save()

            # Get selected tracks from POST data (JSON string)
            selected_tracks_json = request.POST.get('selected_tracks_json', '[]')
            selected_tracks_data_from_post = json.loads(selected_tracks_json)

            for track_data in selected_tracks_data_from_post:
                track_obj, created = Track.objects.update_or_create(
                    spotify_id=track_data['id'],
                    defaults={
                        'title': track_data['name'],
                        'artist': track_data['artist'],
                        'track_url': track_data['url'],
                        'image_url': track_data.get('album_image_url', '')
                    }
                )
                playlist.tracks.add(track_obj)

            messages.success(request, "플레이리스트가 성공적으로 생성되었습니다.")
            return redirect('mypage:index')

    return render(request, 'mypage/create_playlist.html', {'form': form, 'selected_tracks_data': selected_tracks_data})

@login_required
def edit_playlist(request, playlist_id):
    playlist = get_object_or_404(Playlist, pk=playlist_id, user=request.user)
    form = PlaylistForm(instance=playlist)
    selected_tracks_data = []
    for track in playlist.tracks.all():
        # Fetch full track details from Spotify API to get album_image_url
        try:
            print(f"[DEBUG] Fetching details for Spotify ID: {track.spotify_id}")
            spotify_track = spotify_client.track(track.spotify_id)
            album_image_url = None
            if spotify_track:
                print(f"[DEBUG] Spotify track data received: {spotify_track.keys()}")
                if 'album' in spotify_track and spotify_track['album'] and 'images' in spotify_track['album'] and spotify_track['album']['images']:
                    album_image_url = spotify_track['album']['images'][0]['url']
                    print(f"[DEBUG] Album image URL extracted: {album_image_url}")
                else:
                    print("[DEBUG] No album images found for this track.")
            else:
                print("[DEBUG] spotify_client.track returned None.")

            selected_tracks_data.append({
                'id': track.spotify_id,
                'name': spotify_track['name'],
                'artist': spotify_track['artists'][0]['name'] if spotify_track['artists'] else 'Unknown Artist',
                'url': spotify_track['external_urls']['spotify'],
                'album_image_url': album_image_url
            })
        except Exception as e:
            print(f"Error fetching Spotify track {track.spotify_id}: {e}")
            # Fallback if Spotify API call fails
            selected_tracks_data.append({
                'id': track.spotify_id,
                'name': track.title,
                'artist': track.artist,
                'url': track.track_url,
                'album_image_url': ''
            })

    if request.method == 'POST':
        form = PlaylistForm(request.POST, instance=playlist)
        if form.is_valid():
            form.save()

            # Update tracks in the playlist
            selected_tracks_json = request.POST.get('selected_tracks_json', '[]')
            selected_tracks_data = json.loads(selected_tracks_json)

            playlist.tracks.clear() # Clear existing tracks
            for track_data in selected_tracks_data:
                track_obj, created = Track.objects.get_or_create(
                    spotify_id=track_data['id'],
                    defaults={
                        'title': track_data['name'],
                        'artist': track_data['artist'],
                        'track_url': track_data['url'],
                        'image_url': track_data.get('album_image_url', '')
                    }
                )
                playlist.tracks.add(track_obj)

            messages.success(request, "플레이리스트가 성공적으로 업데이트되었습니다.")
            return redirect('mypage:playlist_detail', playlist_id=playlist.id)

    print(f"[DEBUG] selected_tracks_data before rendering: {selected_tracks_data}")
    return render(request, 'mypage/edit_playlist.html', {'form': form, 'playlist': playlist, 'selected_tracks_data': selected_tracks_data})

@login_required
def playlist_detail(request, playlist_id):
    playlist = get_object_or_404(Playlist, pk=playlist_id, user=request.user)
    
    tracks_with_details = []
    for track in playlist.tracks.all():
        try:
            spotify_track = spotify_client.track(track.spotify_id)
            album_image_url = None
            if spotify_track and spotify_track['album'] and spotify_track['album']['images']:
                album_image_url = spotify_track['album']['images'][0]['url']
            
            tracks_with_details.append({
                'id': track.spotify_id,
                'name': spotify_track['name'] if spotify_track else track.title,
                'artist': spotify_track['artists'][0]['name'] if spotify_track and spotify_track['artists'] else track.artist,
                'url': spotify_track['external_urls']['spotify'] if spotify_track else track.track_url,
                'album_image_url': album_image_url
            })
        except Exception as e:
            print(f"Error fetching Spotify track {track.spotify_id} for detail view: {e}")
            tracks_with_details.append({
                'id': track.spotify_id,
                'name': track.title,
                'artist': track.artist,
                'url': track.track_url,
                'album_image_url': '' # Fallback to empty if API fails
            })

    return render(request, 'mypage/playlist_detail.html', {'playlist': playlist, 'tracks_with_details': tracks_with_details})

@login_required
def delete_playlist(request, playlist_id):
    playlist = get_object_or_404(Playlist, pk=playlist_id, user=request.user)
    if request.method == 'POST':
        playlist.delete()
        messages.success(request, "플레이리스트가 성공적으로 삭제되었습니다.") # Add success message
        return redirect('mypage:index')
    # No need to render a separate confirmation page anymore
    return redirect('mypage:playlist_detail', playlist_id=playlist_id) # Redirect back if GET request (shouldn't happen with modal)

@login_required
def listening_history(request):
    history = ListeningHistory.objects.filter(user=request.user).order_by('-listened_at')
    return render(request, 'mypage/listening_history.html', {'history': history})

@csrf_exempt # AJAX POST 요청을 위해 CSRF 예외 처리 (실제 서비스에서는 더 안전한 방법 고려)
@require_POST # POST 요청만 허용
@login_required
def record_listening_history(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            spotify_id = data.get('spotify_id')
            title = data.get('title')
            artist = data.get('artist')
            track_url = data.get('track_url')

            if not all([spotify_id, title, artist, track_url]):
                return JsonResponse({'status': 'error', 'message': 'Missing data'}, status=400)

            # Track 모델에서 해당 곡을 찾거나 생성
            track, created = Track.objects.get_or_create(
                spotify_id=spotify_id,
                defaults={'title': title, 'artist': artist, 'track_url': track_url}
            )

            # ListeningHistory에 기록
            ListeningHistory.objects.create(
                user=request.user,
                track=track
            )
            return JsonResponse({'status': 'success'})
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)

@require_POST
@login_required
def clear_listening_history(request):
    ListeningHistory.objects.filter(user=request.user).delete()
    messages.success(request, "청취 기록이 성공적으로 초기화되었습니다.")
    return redirect('mypage:listening_history')

@login_required
def search_spotify_tracks(request):
    query = request.GET.get('q', '')
    if not query:
        return JsonResponse({'tracks': []})

    try:
        # Use the initialized spotify_client
        results = spotify_client.search(q=query, type='track', limit=10)
        tracks_data = []
        if results and results['tracks']['items']:
            for track in results['tracks']['items']:
                album_image_url = None
                if track['album'] and track['album']['images']:
                    album_image_url = track['album']['images'][0]['url']
                tracks_data.append({
                    'id': track['id'],
                    'name': track['name'],
                    'artist': track['artists'][0]['name'] if track['artists'] else 'Unknown Artist',
                    'url': track['external_urls']['spotify'],
                    'album_image_url': album_image_url
                })
        return JsonResponse({'tracks': tracks_data})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)