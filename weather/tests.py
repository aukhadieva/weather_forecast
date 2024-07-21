from django.urls import reverse
from rest_framework import test, status

from users.models import User
from weather.models import Weather


class UserAPITestCase(test.APITestCase):
    """
    Класс для тестирования эндпоинтов модели User.
    """

    def setUp(self):
        self.user = User.objects.create(email='test@bk.ru', password=123)
        self.client.force_authenticate(user=self.user)
        self.weather = Weather.objects.create(user=self.user, location='location')

    def test_weather_list(self):
        """
        Тест на получение списка погоды.
        """
        url = reverse('weather:weather_list')
        response = self.client.get(url)
        data = response.json()
        result = {
            'count': 1,
            'next': None,
            'previous': None,
            'results': [
                {'id': self.weather.pk,
                 'locations_count': 1,
                 'location': self.weather.location,
                 'temperature': None,
                 'datetime': None,
                 'user': self.user.pk}
            ]
        }
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, result)

    def test_weather_retrieve(self):
        """
        Тест на получение одной объекта погоды.
        """
        url = reverse('weather:weather_detail', args=(self.weather.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get('location'), self.weather.location)
