from django.db.models import Prefetch
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework.response import Response
from rest_framework.views import APIView

from jobs.models import Job
from matching.models import MatchResult

from .models import Application
from .serializers import ApplicationSerializer


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
