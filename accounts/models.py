import random

from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.

class UserRole(models.TextChoices):
    ADMIN = "ADMIN", "Admin"
    DIRECTOR = 'DIRECTOR', "Director"
    TEACHER = "TEACHER", "Teacher"
    STUDENT = "STUDENT", "Student"


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email must be set")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault('role', UserRole.ADMIN)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, blank=False, null=False)
    first_name = models.CharField(max_length=20, blank=False, null=False)
    last_name = models.CharField(max_length=20, blank=False, null=False)
    role = models.CharField(max_length=16, choices=UserRole.choices, default=UserRole.STUDENT)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class DirectorProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='director_profile'
    )
    contact_phone = models.CharField(max_length=32, blank=True, default='')
    contact_telegram = models.CharField(max_length=64, blank=True, default='')
    note = models.CharField(max_length=200, blank=True, default='')

    def __str__(self):
        return f"DirectorProfile({self.user.first_name} {self.user.last_name})"


class TeacherProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='teacher_profile'
    )
    bio = models.TextField(blank=True, default='')
    experience_years = models.PositiveSmallIntegerField(null=True, blank=True)

    def __str__(self):
        return f"TeacherProfile({self.user.first_name} {self.user.last_name})"


def generate_unique_exam_code():
    from .models import StudentProfile
    while True:
        code = str(random.randint(1000, 9999))
        if not StudentProfile.objects.filter(exam_code=code).exists():
            return code


class StudentProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="student_profile"
    )
    exam_code = models.CharField(max_length=4, unique=True, editable=False)
    age = models.PositiveSmallIntegerField(null=True, blank=True)
    school_grade = models.CharField(max_length=20, blank=True, default="")

    def save(self, *args, **kwargs):
        if not self.exam_code:
            self.exam_code = generate_unique_exam_code()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"StudentProfile({self.user.first_name}, {self.user.last_name})"


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_role_profiles(sender, instance, created, **kwargs):
    if not created:
        return
    role = getattr(instance, 'role', None)
    if role == UserRole.DIRECTOR:
        DirectorProfile.objects.create(user=instance)
    elif role == UserRole.TEACHER:
        TeacherProfile.objects.create(user=instance)
    elif role == UserRole.STUDENT:
        StudentProfile.objects.create(user=instance)
