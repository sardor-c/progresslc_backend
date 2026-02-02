from django.conf import settings
from django.db import models

# Create your models here.

class LearningCentre(models.Model):
    director = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='centers'
    )

    name = models.CharField(max_length=200)
    specialization = models.CharField(max_length=200, blank=True, default='')
    description = models.TextField(blank=True, default='')

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [('director', 'name')]

    def __str__(self):
        return f"{self.name} ({self.director.full_name})"

