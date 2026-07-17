import uuid

from django.db import models

from applications.models import Application


class GeneratedDocument(models.Model):
    class DocType(models.TextChoices):
        TAILORED_RESUME = "tailored_resume"
        COVER_LETTER = "cover_letter"
        INTERVIEW_PREP = "interview_prep"
        ROADMAP = "roadmap"
        SKILL_GAP = "skill_gap"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    application = models.ForeignKey(Application, on_delete=models.CASCADE, related_name="documents")
    doc_type = models.CharField(max_length=30, choices=DocType.choices)
    content = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Doc<{self.doc_type} for {self.application_id}>"
