from django.urls import path

from .views import ResumeDetailView, ResumeUploadView

urlpatterns = [
    path("resumes/upload", ResumeUploadView.as_view(), name="resume-upload"),
    path("resumes/<uuid:pk>", ResumeDetailView.as_view(), name="resume-detail"),
]
