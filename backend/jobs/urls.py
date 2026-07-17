from django.urls import path

from .views import JobDetailView, JobDiscoverView, JobListView

urlpatterns = [
    path("jobs", JobListView.as_view(), name="job-list"),
    path("jobs/discover", JobDiscoverView.as_view(), name="job-discover"),
    path("jobs/<uuid:pk>", JobDetailView.as_view(), name="job-detail"),
]
