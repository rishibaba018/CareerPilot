import uuid

from django.db import models

from jobs.models import Job
from profiles.models import Profile


class MatchResult(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="match_results")
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name="match_results")
    fit_score = models.IntegerField()
    reasoning = models.TextField(blank=True)
    matched_skills = models.JSONField(default=list, blank=True)
    missing_skills = models.JSONField(default=list, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("profile", "job")

    def __str__(self):
        return f"Match<{self.profile.user.email} x {self.job.title}: {self.fit_score}>"
