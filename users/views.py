from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic import CreateView
from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated

from common.mixins import TitleMixin
from users.forms import UserLoginForm, UserRegistrationForm
from users.models import User
from users.permissions import IsUser
from users.serializers import UserSerializer, UserListSerializer


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


class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet для модели User.
    """
    queryset = User.objects.all()

    def get_permissions(self):
        """
        Проверяет права и исходя из этого разрешает / запрещает доступ эндпоинтам
        и определяет сериализатор.
        """
        if self.action == "create":
            self.permission_classes = [AllowAny]
            self.serializer_class = UserSerializer
        if self.action in ["list"]:
            self.permission_classes = [IsAuthenticated]
            self.serializer_class = UserListSerializer
        if self.action in ["retrieve"]:
            self.permission_classes = [IsAuthenticated, IsUser]
            self.serializer_class = UserSerializer
        if self.action in ["update", "partial_update", "destroy"]:
            self.permission_classes = [IsAuthenticated, IsUser]
            self.serializer_class = UserSerializer
        return super().get_permissions()

    def perform_create(self, serializer):
        """
        Хэширует создаваемый при регистрации пароль.
        """
        instance = serializer.save(is_active=True)
        instance.set_password(instance.password)
        instance.save()

    def perform_update(self, serializer):
        """
        Хэширует редактируемый пароль.
        """
        instance = serializer.save()
        instance.set_password(instance.password)
        instance.save()
