import requests
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


def translate_word(word, source_lang='en', target_lang='ru'):
    """
    Переводит слово с source_lang на target_lang используя LibreTranslate API.
    Возвращает переведённый текст или None в случае ошибки.
    """
    url = f"{settings.LIBRETRANSLATE_URL}/translate"
    payload = {
        'q': word,
        'source': source_lang,
        'target': target_lang,
        'format': 'text'
    }
    try:
        response = requests.post(url, json=payload, timeout=5)
        response.raise_for_status()
        return response.json().get('translatedText')
    except requests.exceptions.RequestException as e:
        # Логируем ошибки (убрать потом).
        logger.error(f"Ошибка перевода слова '{word}': {e}")
        return None
