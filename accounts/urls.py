from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView

from accounts.views import RegisterView, MeView, RoleTokenObtainPairView

urlpatterns = [
    path('auth/register/', RegisterView.as_view()),
    path('auth/login/', RoleTokenObtainPairView.as_view()),
    path('auth/refresh/', TokenRefreshView.as_view()),
    path('auth/me/', MeView.as_view()),
]
