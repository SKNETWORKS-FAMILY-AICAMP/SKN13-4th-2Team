from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.conf import settings
from django.views.decorators.http import require_POST
from mypage.models import Playlist, Track
from django.shortcuts import get_object_or_404

@login_required
def index(request):
    return render(request, 'search/index.html')

def spotify_search(request):
    query = request.GET.get('q', '')
    search_type = request.GET.get('type', 'track')  # 'track', 'artist', 'album'
    if not query:
        return JsonResponse({'error': '검색어가 필요합니다.'}, status=400)

    import spotipy
    from spotipy.oauth2 import SpotifyClientCredentials
    sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
        client_id=settings.SPOTIPY_CLIENT_ID,
        client_secret=settings.SPOTIPY_CLIENT_SECRET
    ))

    try:
        results = sp.search(q=query, type=search_type, limit=10)
        output = []

        if search_type == 'track':
            for track in results['tracks']['items']:
                output.append({
                    'id': track['id'],
                    'name': track['name'],
                    'artist': track['artists'][0]['name'] if track['artists'] else '',
                    'album_image': track['album']['images'][0]['url'] if track['album']['images'] else '',
                    'url': track['external_urls']['spotify'],
                })
        elif search_type == 'artist':
            for artist in results['artists']['items']:
                output.append({
                    'id': artist['id'],
                    'name': artist['name'],
                    'image': artist['images'][0]['url'] if artist['images'] else '',
                    'url': artist['external_urls']['spotify'],
                })
        elif search_type == 'album':
            for album in results['albums']['items']:
                output.append({
                    'id': album['id'],
                    'name': album['name'],
                    'artist': album['artists'][0]['name'] if album['artists'] else '',
                    'image': album['images'][0]['url'] if album['images'] else '',
                    'url': album['external_urls']['spotify'],
                })
        return JsonResponse({'results': output})

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@login_required
@require_POST
def add_track_to_playlist(request):
    playlist_id = request.POST.get('playlist_id')
    track_id = request.POST.get('track_id')
    track_name = request.POST.get('track_name')
    artist_name = request.POST.get('artist_name')
    album_image = request.POST.get('album_image')

    try:
        playlist = Playlist.objects.get(id=playlist_id, user=request.user)
        track, created = Track.objects.get_or_create(
            spotify_id=track_id,
            defaults={
                'title': track_name,
                'artist': artist_name,
                'image_url': album_image
            }
        )
        # 이미 존재하는 트랙이라면 image_url을 업데이트
        if not created and track.image_url != album_image:
            track.image_url = album_image
            track.save()

        playlist.tracks.add(track)
        return JsonResponse({'status': 'success', 'message': '트랙이 플레이리스트에 추가되었습니다.'})
    except Playlist.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': '플레이리스트를 찾을 수 없습니다.'}, status=404)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

@login_required
@require_POST
def remove_track_from_playlist(request):
    playlist_id = request.POST.get('playlist_id')
    track_id = request.POST.get('track_id')

    try:
        playlist = get_object_or_404(Playlist, id=playlist_id, user=request.user)
        track = get_object_or_404(Track, spotify_id=track_id)
        playlist.tracks.remove(track)
        return JsonResponse({'status': 'success', 'message': '트랙이 플레이리스트에서 제거되었습니다.'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)