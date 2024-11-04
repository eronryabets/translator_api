from rest_framework import serializers


class TranslateWordSerializer(serializers.Serializer):
    word = serializers.CharField(max_length=999)
    source_lang = serializers.CharField(max_length=10, default='en', required=False)
    target_lang = serializers.CharField(max_length=10, default='ru', required=False)
