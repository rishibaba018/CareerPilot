from django.urls import path

from .views import ApplicationListCreateView, ApplicationUpdateView

urlpatterns = [
    path("applications", ApplicationListCreateView.as_view(), name="applications"),
    path("applications/<uuid:pk>", ApplicationUpdateView.as_view(), name="application-update"),
]
