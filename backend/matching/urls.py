from django.urls import path

from .views import MatchJobView

urlpatterns = [
    path("jobs/<uuid:job_id>/match", MatchJobView.as_view(), name="job-match"),
]
