from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import TemplateView, DetailView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from common.mixins import TitleMixin
from weather.models import Weather
from weather.paginators import WeatherPaginator
from weather.permissions import IsOwner
from weather.serializers import WeatherSerializer
from weather.services import get_weather


class MainTemplateView(TitleMixin, LoginRequiredMixin, TemplateView):
    title = 'Главная'
    template_name = 'weather/weather_search.html'

    def get_success_url(self):
        weather = self.get_object()
        return reverse('weather:weather_detail', args=[weather.pk])

    def post(self, request):
        """
        Обрабатывает запрос погоды.
        """
        if self.request.method == 'POST':
            location = self.request.POST.get('location')
            response = get_weather(location)

            instance = Weather.objects.create(location=location, temperature=response[1], datetime=response[0],
                                              user=self.request.user)
            instance.save()

        return render(self.request, self.template_name)

    def get_context_data(self, **kwargs):
        """
        Возвращает данные контекста для отображения погоды.
        """
        context = super().get_context_data(**kwargs)
        context['current_weather'] = Weather.objects.filter(user=self.request.user).last()
        # context['last_weather'] = Weather.objects.filter(user=self.request.user).order_by('datetime')[:1]
        return context


class WeatherDetailView(LoginRequiredMixin, DetailView):
    """
    Выводит подробную информацию о погоде.
    """
    model = Weather
    template_name = 'weather/weather_search.html'


class WeatherListAPIView(generics.ListAPIView):
    """
    Эндпоинт модели Weather на получение списка погоды всех пользователей.
    """
    serializer_class = WeatherSerializer
    queryset = Weather.objects.all()
    pagination_class = WeatherPaginator
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ('location',)


class WeatherRetrieveAPIView(generics.RetrieveAPIView):
    """
    Эндпоинт модели Habit на получение одного экземпляра погоды.
    """
    serializer_class = WeatherSerializer
    queryset = Weather.objects.all()
    permission_classes = (IsAuthenticated, IsOwner)
