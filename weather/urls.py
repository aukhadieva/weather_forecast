from django.urls import path

from weather.apps import WeatherConfig
from weather.views import MainTemplateView, WeatherDetailView, WeatherListAPIView, WeatherRetrieveAPIView

app_name = WeatherConfig.name

urlpatterns = [
    path('', MainTemplateView.as_view(), name='home_page'),
    path('weather/<int:pk>/', WeatherDetailView.as_view(), name='current_weather'),
    path('weather_list/', WeatherListAPIView.as_view(), name='weather_list'),
    path('weather_detail/<int:pk>/', WeatherRetrieveAPIView.as_view(), name='weather_detail'),
]
