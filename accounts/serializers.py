from django.contrib.auth import get_user_model
from rest_framework import serializers

from accounts.models import UserRole, DirectorProfile, TeacherProfile, StudentProfile

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


class DirectorProfileSerialization(serializers.ModelSerializer):
    class Meta:
        model = DirectorProfile
        fields = ('contact_phone', 'contact_telegram', 'note')


class TeacherProfileSerialization(serializers.ModelSerializer):
    class Meta:
        model = TeacherProfile
        fields = ('bio', 'experience_years')


class StudentProfileSerialization(serializers.ModelSerializer):
    class Meta:
        model = StudentProfile
        fields = ('age', 'school_grade', 'exam_code')
        read_only_fields = ('exam_code',)


class MeSerializer(serializers.ModelSerializer):
    director_profile = DirectorProfileSerialization(read_only=True)
    teacher_profile = TeacherProfileSerialization(read_only=True)
    student_profile = StudentProfileSerialization(read_only=True)

    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'first_name',
            'last_name',
            'role',
            'director_profile',
            'teacher_profile',
            'student_profile',
        )

    def to_representation(self, instance):
        data = super().to_representation(instance)
        role = instance.role

        if role == UserRole.DIRECTOR:
            data.pop('teacher_profile', None)
            data.pop('student_profile', None)
        elif role == UserRole.TEACHER:
            data.pop('director_profile', None)
            data.pop('student_profile', None)
        elif role == UserRole.STUDENT:
            data.pop('director_profile', None)
            data.pop('teacher_profile', None)
        else:
            data.pop('director_profile', None)
            data.pop('teacher_profile', None)
            data.pop('student_profile', None)

        return data
