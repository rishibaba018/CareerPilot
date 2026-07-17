from rest_framework import serializers

from matching.models import MatchResult

from .models import Job


class JobSerializer(serializers.ModelSerializer):
    my_match = serializers.SerializerMethodField()

    class Meta:
        model = Job
        fields = (
            "id",
            "title",
            "company",
            "location",
            "description",
            "skills_required",
            "salary_range",
            "work_mode",
            "url",
            "posted_at",
            "my_match",
        )

    def get_my_match(self, job):
        user = self.context["request"].user
        match = next(
            (m for m in job.match_results.all() if m.profile.user_id == user.id), None
        )
        if not match:
            return None
        return {
            "fit_score": match.fit_score,
            "reasoning": match.reasoning,
            "matched_skills": match.matched_skills,
            "missing_skills": match.missing_skills,
        }
