from django.contrib.auth import get_user_model
from django.shortcuts import render
from rest_framework import generics, permissions
from rest_framework_simplejwt.views import TokenObtainPairView

from accounts.models import UserRole, DirectorProfile, TeacherProfile, StudentProfile
from accounts.serializers import RegisterSerializer, MeSerializer
from accounts.tokens import RoleTokenObtainPairSerializer


# Create your views here.

class RoleTokenObtainPairView(TokenObtainPairView):
    serializer_class = RoleTokenObtainPairSerializer


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]


User = get_user_model()

class MeView(generics.RetrieveAPIView):
    serializer_class = MeSerializer

    def get_object(self):
        qs = User.objects.select_related('director_profile', 'teacher_profile', 'student_profile')
        user = qs.get(pk = self.request.user.pk)

        if user.role == UserRole.DIRECTOR:
            DirectorProfile.objects.get_or_create(user=user)
            user = qs.get(pk=user.pk)
        elif user.role == UserRole.TEACHER:
            TeacherProfile.objects.get_or_create(user=user)
            user = qs.get(pk=user.pk)
        elif user.role == UserRole.STUDENT:
            StudentProfile.objects.get_or_create(user=user)
            user = qs.get(pk=user.pk)

        return user
