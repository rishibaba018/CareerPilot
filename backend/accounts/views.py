import logging

from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import RegisterSerializer, UserSerializer

logger = logging.getLogger(__name__)


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response(
            {
                "user": UserSerializer(user).data,
                "access": str(refresh.access_token),
                "refresh": str(refresh),
            },
            status=201,
        )


class GoogleLoginView(APIView):
    """POST /auth/google — sign in with a Google Identity Services credential.

    Body: {"credential": "<google id_token>"}. Verifies the token against
    GOOGLE_CLIENT_ID, then creates-or-logs-in the user by their Google email.
    """

    permission_classes = [permissions.AllowAny]

    def post(self, request):
        credential = request.data.get("credential")
        if not credential:
            return Response(
                {"error": {"code": "NO_CREDENTIAL", "message": "Missing Google credential."}},
                status=400,
            )
        if not settings.GOOGLE_CLIENT_ID:
            return Response(
                {"error": {"code": "GOOGLE_DISABLED", "message": "Google login is not configured."}},
                status=501,
            )

        from google.auth.transport import requests as google_requests
        from google.oauth2 import id_token as google_id_token

        try:
            info = google_id_token.verify_oauth2_token(
                credential, google_requests.Request(), settings.GOOGLE_CLIENT_ID
            )
        except ValueError:
            logger.warning("Google token verification failed")
            return Response(
                {"error": {"code": "INVALID_TOKEN", "message": "Google sign-in failed. Try again."}},
                status=401,
            )

        User = get_user_model()
        user, created = User.objects.get_or_create(email=info["email"].lower())
        if created:
            user.set_unusable_password()
            user.save()
        # Ensure a profile exists either way (Google users skip RegisterSerializer)
        from profiles.models import Profile

        profile, _ = Profile.objects.get_or_create(user=user)
        if not profile.full_name and info.get("name"):
            profile.full_name = info["name"]
            profile.save()

        refresh = RefreshToken.for_user(user)
        return Response(
            {
                "user": UserSerializer(user).data,
                "access": str(refresh.access_token),
                "refresh": str(refresh),
                "created": created,
            }
        )


class MeView(APIView):
    def get(self, request):
        return Response(UserSerializer(request.user).data)
