from rest_framework import viewsets, status
from rest_framework.response import Response
from .utils.translator import translate_word
from .serializers import TranslateWordSerializer


class TranslatorViewSet(viewsets.ViewSet):
    """
    ViewSet для перевода слов с использованием LibreTranslate.
    """

    def create(self, request):
        """
        Обрабатывает POST-запросы на /translate/
        """
        serializer = TranslateWordSerializer(data=request.data)
        if serializer.is_valid():
            word = serializer.validated_data['word']
            source_lang = serializer.validated_data.get('source_lang', 'en')
            target_lang = serializer.validated_data.get('target_lang', 'ru')

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
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
