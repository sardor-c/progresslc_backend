from django.db import transaction

from academics.models import LessonStatus, Lesson, LessonSchedule, Attendance, DayOfWeek
from core.models import GroupMembership


@transaction.atomic
def create_lesson_from_schedule(schedule: LessonSchedule, lesson_date):
    lesson, created = Lesson.objects.get_or_create(
        group=schedule.group,
        date=lesson_date,
        start_time=schedule.start_time,
        defaults={
            "end_time": schedule.end_time,
            "schedule": schedule,
            "status": LessonStatus.PLANNED,
        }
    )

    if created:
        student_ids = (
            GroupMembership.objects
            .filter(group=schedule.group, is_active=True)
            .values_list("student_id", flat=True)
        )

        Attendance.objects.bulk_create(
            [Attendance(lesson=lesson, student_id=sid) for sid in student_ids],
            ignore_conflicts=True
        )

    return lesson


def day_code_from_date(d):
    return [
        DayOfWeek.MO, DayOfWeek.TU, DayOfWeek.WE, DayOfWeek.TH,
        DayOfWeek.FR, DayOfWeek.SA, DayOfWeek.SU
    ][d.weekday()]