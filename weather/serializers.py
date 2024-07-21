from django.db.models import Count
from rest_framework import serializers

from weather.models import Weather


class WeatherSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Habits
    """
    locations_count = serializers.SerializerMethodField()

    class Meta:
        model = Weather
        fields = '__all__'

    def get_locations_count(self, obj):
        """
        Возвращает количество городов.
        """
        return Weather.objects.filter(location=obj.location).count()
