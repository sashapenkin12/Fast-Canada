import requests
from django.conf import settings


def translate_text(text, target_language='en'):
    if not text:
        return text
    url = "https://translation.googleapis.com/language/translate/v2"
    params = {
        "q": text,
        "target": target_language,
        "key": settings.GOOGLE_API_KEY
    }
    try:
        response = requests.post(url, params=params)
        response.raise_for_status()
        return response.json()['data']['translations'][0]['translatedText']
    except Exception as e:
        return text
