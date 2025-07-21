from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse # Import JsonResponse
from django.conf import settings # Import settings
import requests # Import requests

@login_required
def index(request):
    return render(request, 'search/index.html')

def youtube_search(request):
    query = request.GET.get('q', '')
    if not query:
        return JsonResponse({'error': 'Search query is required'}, status=400)

    api_key = settings.YOUTUBE_API_KEY
    print(f"DEBUG: YOUTUBE_API_KEY from settings: {api_key}") # 이 줄을 추가합니다.
    if not api_key:
        return JsonResponse({'error': 'YouTube API key is not configured'}, status=500)

    search_url = 'https://www.googleapis.com/youtube/v3/search'
    params = {
        'part': 'snippet',
        'q': query,
        'type': 'video',
        'maxResults': 5, # Limit to 5 results for now
        'key': api_key
    }

    try:
        response = requests.get(search_url, params=params)
        print(f"DEBUG: YouTube API Response Status Code: {response.status_code}") # 이 줄을 추가합니다.
        print(f"DEBUG: YouTube API Response Content: {response.text}") # 이 줄을 추가합니다.
        response.raise_for_status() # Raise an exception for HTTP errors
        data = response.json()

        results = []
        for item in data.get('items', []):
            video_id = item['id']['videoId']
            title = item['snippet']['title']
            thumbnail = item['snippet']['thumbnails']['default']['url'] # Or 'high' for higher quality

            results.append({
                'video_id': video_id,
                'title': title,
                'thumbnail': thumbnail
            })
        return JsonResponse({'results': results})

    except requests.exceptions.RequestException as e:
        return JsonResponse({'error': f'YouTube API request failed: {e}'}, status=500)
    except Exception as e:
        return JsonResponse({'error': f'An unexpected error occurred: {e}'}, status=500)
