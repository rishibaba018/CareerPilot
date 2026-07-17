import uuid

from django.conf import settings
from django.db import models

from jobs.models import Job


class Application(models.Model):
    class Status(models.TextChoices):
        SAVED = "saved"
        APPLIED = "applied"
        INTERVIEW = "interview"
        OFFER = "offer"
        REJECTED = "rejected"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="applications")
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name="applications")
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.SAVED)
    notes = models.TextField(blank=True)
    applied_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("user", "job")

    def __str__(self):
        return f"App<{self.user.email} -> {self.job.title}: {self.status}>"
