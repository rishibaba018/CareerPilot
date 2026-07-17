from rest_framework import serializers

from .models import Application


class ApplicationSerializer(serializers.ModelSerializer):
    job = serializers.SerializerMethodField()
    job_id = serializers.UUIDField(write_only=True)

    class Meta:
        model = Application
        fields = ("id", "job", "job_id", "status", "notes", "applied_at", "updated_at")
        read_only_fields = ("id", "job", "applied_at", "updated_at")

    def get_job(self, app):
        my_match = next(iter(app.job.match_results.all()), None)
        return {
            "id": app.job.id,
            "title": app.job.title,
            "company": app.job.company,
            "location": app.job.location,
            "work_mode": app.job.work_mode,
            "fit_score": my_match.fit_score if my_match else None,
        }
