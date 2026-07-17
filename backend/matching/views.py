import logging

from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from agents.base import AgentError
from agents.orchestrator import run_matching
from jobs.models import Job
from profiles.serializers import ProfileSerializer

from .models import MatchResult

logger = logging.getLogger(__name__)


class MatchJobView(APIView):
    """POST /jobs/{id}/match — run the Matching Agent and persist the result.

    Cached: re-POSTing returns the saved result unless ?refresh=1 (master-plan
    §19: never regenerate what's saved).
    """

    def post(self, request, job_id):
        job = get_object_or_404(Job, pk=job_id)
        profile = request.user.profile

        existing = MatchResult.objects.filter(profile=profile, job=job).first()
        if existing and request.query_params.get("refresh") != "1":
            return Response(self._payload(existing, cached=True))

        try:
            result = run_matching(
                ProfileSerializer(profile).data,
                {
                    "title": job.title,
                    "company": job.company,
                    "skills_required": job.skills_required,
                    "description": job.description,
                },
            )
        except AgentError:
            logger.exception("Matching Agent failed")
            return Response(
                {"error": {"code": "AI_TIMEOUT", "message": "Our AI is busy, please retry."}},
                status=503,
            )

        match, _ = MatchResult.objects.update_or_create(
            profile=profile,
            job=job,
            defaults={
                "fit_score": int(result.get("fit_score", 0)),
                "reasoning": result.get("reasoning", ""),
                "matched_skills": result.get("matched_skills", []),
                "missing_skills": result.get("missing_skills", []),
            },
        )
        return Response(self._payload(match, cached=False), status=201)

    @staticmethod
    def _payload(match, cached):
        return {
            "fit_score": match.fit_score,
            "reasoning": match.reasoning,
            "matched_skills": match.matched_skills,
            "missing_skills": match.missing_skills,
            "cached": cached,
        }
