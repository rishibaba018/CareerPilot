from django.urls import path

from .views import ApplicationListCreateView, ApplicationUpdateView, PipelineInsightsView

urlpatterns = [
    path("applications", ApplicationListCreateView.as_view(), name="applications"),
    path("applications/insights", PipelineInsightsView.as_view(), name="application-insights"),
    path("applications/<uuid:pk>", ApplicationUpdateView.as_view(), name="application-update"),
]
