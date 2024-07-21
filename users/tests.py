from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse
from rest_framework import test, status

from users.models import User


class UserAPITestCase(test.APITestCase):
    """
    Класс для тестирования эндпоинтов модели User.
    """

    def setUp(self):
        self.user = User.objects.create(email='test@bk.ru', password=123)
        self.client.force_authenticate(user=self.user)

    def test_user_create(self):
        """
        Тест на создание пользователя.
        """
        url = reverse('users:users-list')
        data = {'email': 'test1@bk.ru', 'password': 1234}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.all().count(), 2)

    def test_user_update(self):
        """
        Тест на обновление пользователя.
        """
        url = reverse('users:users-detail', args=(self.user.pk,))
        data = {'email': 'test1@bk.ru', 'password': 123}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get('email'), 'test1@bk.ru')

    def test_user_list(self):
        """
        Тест на получение списка пользователей.
        """
        url = reverse('users:users-list')
        response = self.client.get(url)
        data = response.json()
        result = [{'email': 'test@bk.ru'}]
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, result)

    def test_user_retrieve(self):
        """
        Тест на получение одного пользователя.
        """
        url = reverse('users:users-detail', args=(self.user.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get('email'), self.user.email)

    def test_user_destroy(self):
        """
        Тест на удаление одного пользователя.
        """
        url = reverse('users:users-detail', args=(self.user.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(User.objects.all().count(), 0)


class UserTestCase(TestCase):
    """
    Класс для тестирования регистрации и авторизации пользователей.
    """

    def setUp(self):
        self.path = reverse('users:register')
        self.data = {'email': 'test@bk.ru', 'password1': 123, 'password2': 123}

    def test_user_register(self):
        """
        Тест на регистрацию пользователя.
        """
        response = self.client.get(self.path)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context_data['title'], 'Регистрация')
        self.assertTemplateNotUsed(response, 'register')

    def test_user_login(self):
        """
        Тест на авторизацию пользователя.
        """
        data = {'email': self.data['email'], 'password': self.data['password1']}
        response = self.client.post(reverse('users:login'), data)
        self.assertEqual(response.status_code, HTTPStatus.OK)
