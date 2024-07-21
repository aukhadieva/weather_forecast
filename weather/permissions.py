from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    """
    Проверяет, является ли пользователь - создателем запроса погоды.
    """
    def has_object_permission(self, request, view, obj):
        if obj.user == request.user:
            return True
        return False
