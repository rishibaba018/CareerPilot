from django.urls import path

from .views import CoverLetterView, DocumentDownloadView, OptimizeResumeView

urlpatterns = [
    path("jobs/<uuid:job_id>/optimize-resume", OptimizeResumeView.as_view(), name="optimize-resume"),
    path("jobs/<uuid:job_id>/cover-letter", CoverLetterView.as_view(), name="cover-letter"),
    path("documents/<uuid:pk>/download", DocumentDownloadView.as_view(), name="document-download"),
]
