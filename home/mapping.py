# 감정 기반 태그 (Mood)
MOOD_TAG_MAPPING = {
    "슬픔": "sad",
    "슬픈": "sad",
    "우울": "melancholy",
    "행복": "happy",
    "신남": "energetic",
    "신나는": "energetic",
    "차분함": "calm",
    "사랑": "romantic",
    "이별": "breakup",
    "분노": "angry",
    "감성": "emotional",
    "몽환": "dreamy",
    "위로": "comfort",
    "비": "rainy",
    "여름": "summer",
    "겨울": "winter",
    "구름":"cloudy",
}

# 장르 기반 태그 (Genre)
GENRE_TAG_MAPPING = {
    "케이팝": "k-pop",
    "한국": "k-pop",
    "일본": "j-pop",
    "제이팝": "j-pop",
    "팝": "pop",
    "록": "rock",
    "힙합": "hip-hop",
    "재즈": "jazz",
    "클래식": "classical music",
    "댄스": "dance",
    "알앤비": "rnb",
    "메탈": "metal",
    "인디": "indie",
    "포크": "folk",
    "펑크": "punk",
    "일렉트로닉": "electronic",
    "어쿠스틱": "acoustic"

}

WEATHER_TO_MOOD_TAGS = {
    "맑음": ["sun", "happy", "energetic", "bright"],
    "흐림": ["calm", "chill", "relaxed", "neutral"],
    "비": ["rainy", "melancholic", "sad", "emotional"],
    "눈": ["winter", "dreamy", "romantic", "quiet"],
    "천둥번개": ["stormy", "dark", "angry", "intense"],
    "안개": ["foggy", "mysterious", "dreamy", "soft"],
    "더움": ["summer", "energetic", "sweaty", "fun"],
    "추움": ["cold", "winter", "calm", "lonely"],
    "바람": ["windy", "nostalgic", "free", "refreshing"],
    "구름조금": ["calm", "chill", "relaxed", "neutral"]
}