from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta

from academics.models import LessonSchedule
from academics.utils import day_code_from_date, create_lesson_from_schedule  # yoki shu fayl ichida yozing

class Command(BaseCommand):
    help = "Create lessons from schedules near their start time"

    def handle(self, *args, **options):
        now = timezone.localtime()
        today = now.date()
        dow = day_code_from_date(today)

        lead_minutes = 5  # darsdan 5 minut oldin yaratsin
        window_start = (now - timedelta(minutes=1)).time()
        window_end = (now + timedelta(minutes=lead_minutes)).time()

        schedules = LessonSchedule.objects.filter(
            is_active=True,
            group__is_active=True,
            day_of_week=dow,
            start_time__gte=window_start,
            start_time__lte=window_end,
        )

        for sch in schedules:
            create_lesson_from_schedule(sch, today)

        self.stdout.write(self.style.SUCCESS(f"Processed: {schedules.count()} schedules"))
