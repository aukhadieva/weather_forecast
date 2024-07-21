from rest_framework import serializers

from users.models import User


class UserSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели User.
    """

    class Meta:
        model = User
        fields = ('email', 'password',)


class UserListSerializer(serializers.ModelSerializer):
    """
    Сериализатор для списка пользователей.
    """

    class Meta:
        model = User
        fields = ("email",)
