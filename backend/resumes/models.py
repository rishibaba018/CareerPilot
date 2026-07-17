import uuid

from django.db import models

from profiles.models import Profile


class Resume(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="resumes")
    file = models.FileField(upload_to="resumes/")
    parsed_text = models.TextField(blank=True)
    ats_score = models.IntegerField(null=True, blank=True)
    is_master = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Resume<{self.profile.user.email}, master={self.is_master}>"
