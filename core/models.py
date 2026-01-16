import random
import uuid
from django.utils import timezone

from django.db import models


# Create your models here.


class Subject(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.CharField(max_length=20, unique=True)
    name_uz = models.CharField(max_length=20)

    def __str__(self):
        return self.name_uz


def generate_test_id():
    while True:
        val = random.randint(1000, 9999)
        if not Student.objects.filter(test_id=val).exists():
            return str(val)


class Student(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    test_id = models.CharField(max_length=4, default=generate_test_id, unique=True)
    first_name = models.CharField(max_length=30, default="", blank=True)
    last_name = models.CharField(max_length=30, default="", blank=True)
    rating = models.FloatField(default=0.0)

    primary_subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE,
    )
    created_at = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "students"

    def __str__(self):
        return f"{self.first_name} {self.last_name}".strip() or str(self.id)


class Contact(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name="contacts",
        db_index=True
    )

    phone = models.CharField(max_length=13)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'contacts'
        indexes = [models.Index(fields=['student'])]

class Certificate(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name="certificates",
        db_index=True
    )

    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE,
        related_name="certificates",
        db_index=True,
    )

    count = models.FloatField(default=0.0)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "certificates"
        indexes = [
            models.Index(fields=['student']),
            models.Index(fields=['subject']),
        ]


