from django.contrib.auth import get_user_model
from rest_framework import serializers

from accounts.models import UserRole

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8, required=True)

    role = serializers.ChoiceField(
        choices=[UserRole.DIRECTOR, UserRole.TEACHER, UserRole.STUDENT],
        required=True
    )

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'password', 'role')

    @staticmethod
    def validate_role(self, value):
        if value == UserRole.ADMIN:
            raise serializers.ValidationError("Admin role bilan ro'yhatdan o'tish taqiqlangan.")
        return value

    def create(self, validated_data):
        password = validated_data.pop('password')
        role = validated_data.pop('role')

        user = User(**validated_data)
        user.role = role
        user.set_password(password)
        user.save()
        return user


class MeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'role')
