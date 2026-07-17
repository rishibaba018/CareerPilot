from django.urls import path

from .views import (
    CoverLetterView,
    DocumentDownloadView,
    InterviewPrepView,
    OptimizeResumeView,
    ResumeChatView,
    RoadmapView,
    SkillGapView,
)

urlpatterns = [
    path("jobs/<uuid:job_id>/optimize-resume", OptimizeResumeView.as_view(), name="optimize-resume"),
    path("jobs/<uuid:job_id>/cover-letter", CoverLetterView.as_view(), name="cover-letter"),
    path("jobs/<uuid:job_id>/resume-chat", ResumeChatView.as_view(), name="resume-chat"),
    path("jobs/<uuid:job_id>/interview-prep", InterviewPrepView.as_view(), name="interview-prep"),
    path("jobs/<uuid:job_id>/skill-gap", SkillGapView.as_view(), name="skill-gap"),
    path("career/roadmap", RoadmapView.as_view(), name="career-roadmap"),
    path("documents/<uuid:pk>/download", DocumentDownloadView.as_view(), name="document-download"),
]
