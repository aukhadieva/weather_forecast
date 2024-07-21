from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic import CreateView

from common.mixins import TitleMixin
from users.forms import UserLoginForm, UserRegistrationForm
from users.models import User


class UserLoginView(TitleMixin, LoginView):
    """
    Класс-представление для страницы авторизации пользователя.
    """
    model = User
    form_class = UserLoginForm
    template_name = 'users/login.html'
    title = 'Авторизация'


class UserRegisterView(TitleMixin, CreateView):
    """
    Класс-представление для страницы регистрации пользователя.
    """
    model = User
    form_class = UserRegistrationForm
    success_url = reverse_lazy('users:login')
    template_name = 'users/register.html'
    title = 'Регистрация'

    def form_valid(self, form):
        """
        Сохраняет созданного пользователя, а также активирует его.
        """
        user = form.save()
        user.is_active = True
        user.save()
        return super().form_valid(form)
