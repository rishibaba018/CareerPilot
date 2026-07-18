import logging

from django.db.models import Prefetch
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework.response import Response
from rest_framework.views import APIView

from agents.base import AgentError
from agents.orchestrator import run_tracking
from jobs.models import Job
from matching.models import MatchResult

from .models import Application
from .serializers import ApplicationSerializer

logger = logging.getLogger(__name__)


def _queryset(user):
    return (
        Application.objects.filter(user=user)
        .select_related("job")
        .prefetch_related(
            Prefetch(
                "job__match_results",
                queryset=MatchResult.objects.filter(profile__user=user),
            )
        )
        .order_by("-updated_at")
    )


class ApplicationListCreateView(APIView):
    def get(self, request):
        """Dashboard data, grouped by kanban column."""
        grouped = {status: [] for status, _ in Application.Status.choices}
        for app in _queryset(request.user):
            grouped[app.status].append(ApplicationSerializer(app).data)
        return Response(grouped)

    def post(self, request):
        serializer = ApplicationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        job = get_object_or_404(Job, pk=serializer.validated_data["job_id"])
        status_value = serializer.validated_data.get("status", Application.Status.SAVED)

        app, created = Application.objects.get_or_create(
            user=request.user, job=job, defaults={"status": status_value}
        )
        if not created and app.status != status_value:
            app.status = status_value
        if app.status == Application.Status.APPLIED and app.applied_at is None:
            # Submission is SIMULATED (master-plan §2): we record intent honestly.
            app.applied_at = timezone.now()
        app.save()
        return Response(ApplicationSerializer(app).data, status=201 if created else 200)


class PipelineInsightsView(APIView):
    """GET /applications/insights — Tracking Agent coaching over the pipeline."""

    def get(self, request):
        apps = list(_queryset(request.user))
        if not apps:
            return Response(
                {
                    "insights": ["Your pipeline is empty — nothing to analyze yet."],
                    "suggestions": [
                        "Browse the job feed and save 3-5 roles that fit you.",
                        "Run 'Analyze my fit' on each to see where you stand.",
                    ],
                }
            )

        now = timezone.now()
        payload = []
        for app in apps:
            match = next(iter(app.job.match_results.all()), None)
            payload.append(
                {
                    "job": f"{app.job.title} at {app.job.company}",
                    "status": app.status,
                    "days_in_status": (now - app.updated_at).days,
                    "fit_score": match.fit_score if match else None,
                }
            )
        try:
            result = run_tracking(payload, request.user.profile.preferences)
        except AgentError:
            logger.exception("Tracking Agent failed")
            return Response(
                {"error": {"code": "AI_TIMEOUT", "message": "Our AI is busy, please retry."}},
                status=503,
            )
        return Response(result)


class ApplicationUpdateView(APIView):
    def patch(self, request, pk):
        app = get_object_or_404(Application, pk=pk, user=request.user)
        serializer = ApplicationSerializer(app, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        app = serializer.save()
        if app.status == Application.Status.APPLIED and app.applied_at is None:
            app.applied_at = timezone.now()
            app.save()
        return Response(ApplicationSerializer(app).data)
