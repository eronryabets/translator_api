from rest_framework import viewsets, status
from rest_framework.response import Response
from .utils.translator import translate_word


class TranslatorViewSet(viewsets.ViewSet):
    """
    ViewSet для перевода слов с использованием LibreTranslate.
    """

    def list(self, request):
        """
        Обрабатывает GET-запросы на /translate/
        """
        word = request.query_params.get('word', '').strip()
        source_lang = request.query_params.get('source_lang', 'en').strip()
        target_lang = request.query_params.get('target_lang', 'ru').strip()

        if not word:
            return Response(
                {"error": "Слово для перевода не указано."},
                status=status.HTTP_400_BAD_REQUEST
            )

        translation = translate_word(word, source_lang, target_lang)

        if translation:
            return Response(
                {"word": word, "translation": translation},
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                {"error": "Не удалось выполнить перевод."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
