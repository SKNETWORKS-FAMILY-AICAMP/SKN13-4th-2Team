from .mapping import MOOD_TAG_MAPPING, GENRE_TAG_MAPPING

def extract_tags_from_text(text):
    text = text.lower()
    mood_tag = next((en for kr, en in MOOD_TAG_MAPPING.items() if kr in text), None)
    genre_tag = next((en for kr, en in GENRE_TAG_MAPPING.items() if kr in text), None)
    return mood_tag, genre_tag
