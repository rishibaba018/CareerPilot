import logging

from rest_framework import status
from rest_framework.generics import RetrieveAPIView
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView

from agents.base import AgentError
from agents.orchestrator import run_onboarding
from profiles.serializers import ProfileSerializer

from .models import Resume
from .parsing import UnreadablePDFError, extract_pdf_text
from .serializers import ResumeSerializer

logger = logging.getLogger(__name__)

MAX_SIZE = 5 * 1024 * 1024  # FR-02: max 5 MB


def error_response(code, message, http_status):
    return Response({"error": {"code": code, "message": message}}, status=http_status)


class ResumeUploadView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        file = request.FILES.get("file")
        if not file:
            return error_response("NO_FILE", "Attach a PDF as the 'file' field.", 400)
        if not file.name.lower().endswith(".pdf") or file.content_type not in (
            "application/pdf",
            "application/x-pdf",
        ):
            return error_response("NOT_PDF", "Only PDF resumes are supported.", 400)
        if file.size > MAX_SIZE:
            return error_response("TOO_LARGE", "PDF must be 5 MB or smaller.", 400)

        try:
            text = extract_pdf_text(file)
        except UnreadablePDFError as exc:
            return error_response("UNREADABLE_PDF", str(exc), 422)

        try:
            parsed = run_onboarding(text)
        except AgentError:
            logger.exception("Profile Agent failed")
            return error_response(
                "AI_TIMEOUT", "Our AI is busy, please retry in a moment.", 503
            )

        profile = request.user.profile
        file.seek(0)
        # The latest upload becomes the master resume (users re-upload to replace)
        profile.resumes.update(is_master=False)
        resume = Resume.objects.create(
            profile=profile,
            file=file,
            parsed_text=text,
            ats_score=parsed.get("ats_score"),
            is_master=True,
        )

        # Fill the master profile from extraction, keeping existing user edits
        for field in ("full_name", "phone", "location"):
            if parsed.get(field) and not getattr(profile, field):
                setattr(profile, field, parsed[field])
        for field in ("skills", "education", "experience", "projects"):
            if parsed.get(field):
                setattr(profile, field, parsed[field])
        profile.save()

        return Response(
            {
                "resume": ResumeSerializer(resume).data,
                "profile": ProfileSerializer(profile).data,
                "summary": parsed.get("summary", ""),
                "ats_feedback": parsed.get("ats_feedback", []),
            },
            status=status.HTTP_201_CREATED,
        )


class ResumeDetailView(RetrieveAPIView):
    serializer_class = ResumeSerializer

    def get_queryset(self):
        return Resume.objects.filter(profile__user=self.request.user)
