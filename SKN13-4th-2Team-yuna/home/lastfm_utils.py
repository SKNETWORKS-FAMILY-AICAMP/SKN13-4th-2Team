import pylast
from django.conf import settings
from home.mapping import MOOD_TAG_MAPPING, GENRE_TAG_MAPPING

# Last.fm API 인증 객체 생성
lastfm_network = pylast.LastFMNetwork(
    api_key=settings.LASTFM_API_KEY,
    api_secret=settings.LASTFM_API_SECRET
)

def get_tracks_by_tags(mood_tag=None, genre_tag=None, limit=5):
    """감정 태그와 장르 태그를 모두 만족하는 트랙만 추천 (교집합 방식)"""
    try:
        def fetch_tracks(tag):
            try:
                return lastfm_network.get_tag(tag).get_top_tracks(limit=1000)  # 넉넉히 가져오기
            except Exception:
                return []

        mood_tracks = fetch_tracks(mood_tag) if mood_tag else []
        genre_tracks = fetch_tracks(genre_tag) if genre_tag else []

        # mood, genre 모두 있는 경우 교집합
        if mood_tag and genre_tag:
            mood_set = {f"{t.item.artist.name}_{t.item.title}": t for t in mood_tracks}
            genre_set = {f"{t.item.artist.name}_{t.item.title}": t for t in genre_tracks}
            common_keys = mood_set.keys() & genre_set.keys()

            result = []
            for key in common_keys:
                track = mood_set[key].item  # mood 기준에서 꺼내도 됨
                result.append({
                    'name': track.title,
                    'artist': track.artist.name,
                    'url': track.get_url(),
                    'album_image_url': None
                })
                if len(result) >= limit:
                    break
            return result

        # 한쪽만 있는 경우
        combined = mood_tracks if mood_tag else genre_tracks
        result = []
        seen = set()
        for entry in combined:
            track = entry.item
            key = f"{track.artist.name}_{track.title}"
            if key not in seen:
                seen.add(key)
                result.append({
                    'name': track.title,
                    'artist': track.artist.name,
                    'url': track.get_url(),
                    'album_image_url': None
                })
            if len(result) >= limit:
                break
        return result
    except Exception as e:
        print(f"[오류] Last.fm 태그 검색 실패: {e}")
        return []


def get_similar_tracks_by_artist(artist_name, limit=5):
    """특정 아티스트 이름으로 유사한 아티스트의 트랙 추천"""
    try:
        artist = lastfm_network.get_artist(artist_name)
        similar_artists = artist.get_similar(limit=3)

        tracks = []
        for similar in similar_artists:
            top_tracks = similar.item.get_top_tracks(limit=2)
            for track in top_tracks:
                tracks.append({
                    'name': track.item.title,
                    'artist': track.item.artist.name,
                    'url': track.item.get_url(),
                    'album_image_url': None
                })
                if len(tracks) >= limit:
                    return tracks
        return tracks
    except Exception as e:
        print(f"[오류] Last.fm 유사 아티스트 검색 실패: {e}")
        return []