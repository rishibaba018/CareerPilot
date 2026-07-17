from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.http import JsonResponse
from django.urls import include, path


def health(_request):
    return JsonResponse({"status": "ok", "app": "careerpilot"})


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/health", health),
    path("api/v1/auth/", include("accounts.urls")),
    path("api/v1/", include("profiles.urls")),
    path("api/v1/", include("resumes.urls")),
    path("api/v1/", include("jobs.urls")),
    path("api/v1/", include("matching.urls")),
    path("api/v1/", include("documents.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
