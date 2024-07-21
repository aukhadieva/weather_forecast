from django.contrib import admin

from weather.models import Weather


@admin.register(Weather)
class WeatherAdmin(admin.ModelAdmin):
    """
    Административная панель модели Weather.
    """
    list_display = ('location', 'user',)
