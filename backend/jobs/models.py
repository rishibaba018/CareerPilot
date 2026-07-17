import uuid

from django.db import models


class Job(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    external_id = models.CharField(max_length=255, unique=True, null=True, blank=True)
    title = models.CharField(max_length=255)
    company = models.CharField(max_length=255)
    location = models.CharField(max_length=255, blank=True)
    description = models.TextField()
    skills_required = models.JSONField(default=list, blank=True)
    salary_range = models.CharField(max_length=100, blank=True)
    work_mode = models.CharField(max_length=50, blank=True)
    url = models.URLField(max_length=500, blank=True)
    posted_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} @ {self.company}"
