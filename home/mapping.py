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
    "겨울": "winter"
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
    "클래식": "classical",
    "댄스": "dance",
    "알앤비": "rnb",
    "메탈": "metal",
    "인디": "indie",
    "포크": "folk",
    "펑크": "punk",
    "일렉트로닉": "electronic",
    "어쿠스틱": "acoustic"
}

# 날씨 기반 태그 매핑 (Weather to Mood/Genre)
WEATHER_TO_TAG_MAPPING = {
    "맑음": ["happy", "energetic", "upbeat", "pop"],
    "구름": ["calm", "mellow", "indie"],
    "구름조금": ["calm", "mellow", "indie"],
    "구름많음": ["calm", "mellow", "indie"],
    "흐림": ["calm", "melancholy", "acoustic"],
    "비": ["rainy", "melancholy", "sad", "acoustic", "jazz"],
    "눈": ["winter", "calm", "melancholy", "classical"],
    "천둥번개": ["angry", "rock", "metal"],
    "안개": ["dreamy", "calm", "ambient"],
    "바람": ["energetic", "rock"],
    "소나기": ["rainy", "energetic", "pop"],
    "뇌우": ["angry", "rock", "metal"],
    "우박": ["angry", "rock"],
    "황사": ["calm", "melancholy"],
    "미세먼지": ["calm", "melancholy"],
    "보통": ["calm", "mellow"], # 미세먼지/황사 농도 '보통'일 경우
    "좋음": ["happy", "energetic"], # 미세먼지/황사 농도 '좋음'일 경우
    "나쁨": ["melancholy", "sad"], # 미세먼지/황사 농도 '나쁨'일 경우
    "매우나쁨": ["melancholy", "sad", "angry"], # 미세먼지/황사 농도 '매우나쁨'일 경우
}

