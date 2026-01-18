import uuid

from django.db import models, transaction

from core.models import Group, Student, GroupMembership


# Create your models here.
class DayOfWeek(models.TextChoices):
    MO = "Mo", "Dushanba"
    TU = "Tu", "Seshanba"
    WE = "We", "Chorshanba"
    TH = "Th", "Payshanba"
    FR = "Fr", "Juma"
    SA = "Sa", "Shanba"
    SU = "Su", "Yakshanba"

class LessonSchedule(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="schedules", db_index=True)

    day_of_week = models.CharField(max_length=2, choices=DayOfWeek.choices)
    start_time = models.TimeField()
    end_time = models.TimeField()

    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "lesson_schedules"
        constraints = [
            models.UniqueConstraint(
                fields=["group", "day_of_week", "start_time"],
                name="uniq_schedule_slot"
            ),
        ]
        indexes = [
            models.Index(fields=["day_of_week", "start_time"]),
            models.Index(fields=["group"]),
        ]

    def __str__(self):
        return f"{self.group} {self.day_of_week} {self.start_time}-{self.end_time}"


class LessonStatus(models.TextChoices):
    PLANNED = "planned", "Planned"
    ONGOING = "ongoing", "Ongoing"
    DONE = "done", "Done"
    CANCELED = "canceled", "Canceled"


class Lesson(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="lessons", db_index=True)
    schedule = models.ForeignKey(LessonSchedule, on_delete=models.SET_NULL, null=True, blank=True, related_name="lessons")

    date = models.DateField(db_index=True)
    start_time = models.TimeField()
    end_time = models.TimeField()

    status = models.CharField(max_length=10, choices=LessonStatus.choices, default=LessonStatus.PLANNED)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "lessons"
        constraints = [
            models.UniqueConstraint(fields=["group", "date", "start_time"], name="uniq_group_lesson"),
        ]
        indexes = [
            models.Index(fields=["group", "date"]),
            models.Index(fields=["date", "start_time"]),
        ]

    def __str__(self):
        return f"{self.group} {self.date} {self.start_time}"


class AttendanceStatus(models.TextChoices):
    PRESENT = "present", "Present"
    ABSENT = "absent", "Absent"
    LATE = "late", "Late"
    EXCUSED = "excused", "Excused"


class Attendance(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name="attendances", db_index=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="attendances", db_index=True)

    status = models.CharField(max_length=10, choices=AttendanceStatus.choices, default=AttendanceStatus.ABSENT)
    marked_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "attendances"
        constraints = [
            models.UniqueConstraint(fields=["lesson", "student"], name="uniq_lesson_student_attendance"),
        ]


