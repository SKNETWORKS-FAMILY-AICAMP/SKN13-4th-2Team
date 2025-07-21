from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.conf import settings

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
