from rest_framework import serializers

from weather.models import Weather


class WeatherSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Habits
    """

    class Meta:
        model = Weather
        fields = '__all__'
