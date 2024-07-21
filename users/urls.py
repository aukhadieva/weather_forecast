from django.contrib.auth.views import LogoutView
from django.urls import path
from rest_framework import routers
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users.apps import UsersConfig
from users.views import UserLoginView, UserRegisterView, UserViewSet

app_name = UsersConfig.name

router = routers.DefaultRouter()
router.register(r'users', UserViewSet, basename='users')

urlpatterns = [
    path('', UserLoginView.as_view(), name='login'),
    path('register/', UserRegisterView.as_view(), name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('login/token/', TokenObtainPairView.as_view(permission_classes=[AllowAny]), name='token_obtain'),
    path('refresh/token/', TokenRefreshView.as_view(permission_classes=[AllowAny]), name='token_refresh'),
] + router.urls
