from django.db.models import Prefetch, Q
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from agents.orchestrator import run_discovery
from matching.models import MatchResult

from .models import Job
from .serializers import JobSerializer


def _with_user_matches(queryset, user):
    return queryset.prefetch_related(
        Prefetch(
            "match_results",
            queryset=MatchResult.objects.filter(profile__user=user).select_related("profile"),
        )
    )


class JobListView(ListAPIView):
    serializer_class = JobSerializer

    def get_queryset(self):
        qs = Job.objects.order_by("-posted_at", "-created_at")
        params = self.request.query_params
        if q := params.get("q"):
            qs = qs.filter(
                Q(title__icontains=q) | Q(company__icontains=q) | Q(description__icontains=q)
            )
        if location := params.get("location"):
            qs = qs.filter(location__icontains=location)
        if mode := params.get("mode"):
            qs = qs.filter(work_mode=mode)
        return _with_user_matches(qs, self.request.user)


class JobDetailView(RetrieveAPIView):
    serializer_class = JobSerializer

    def get_queryset(self):
        return _with_user_matches(Job.objects.all(), self.request.user)


class JobDiscoverView(APIView):
    def post(self, request):
        result = run_discovery(request.user.profile.preferences)
        return Response(result)
