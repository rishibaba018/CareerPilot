import logging

from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from agents.base import AgentError
from agents.orchestrator import (
    run_cover_letter,
    run_interview_prep,
    run_matching,
    run_resume_optimizer,
    run_roadmap,
    run_skill_gap,
)
from applications.models import Application
from jobs.models import Job
from matching.models import MatchResult
from profiles.serializers import ProfileSerializer

from .models import GeneratedDocument
from .pdf import render_cover_letter_pdf, render_resume_pdf

logger = logging.getLogger(__name__)

AI_BUSY = {"error": {"code": "AI_TIMEOUT", "message": "Our AI is busy, please retry."}}


def _get_application(user, job):
    """Generating documents for a job implicitly saves it to the pipeline."""
    app, _ = Application.objects.get_or_create(user=user, job=job)
    return app


def _job_payload(job):
    return {
        "title": job.title,
        "company": job.company,
        "skills_required": job.skills_required,
        "description": job.description,
    }


def _cached_doc(application, doc_type, refresh):
    if refresh:
        return None
    return (
        GeneratedDocument.objects.filter(application=application, doc_type=doc_type)
        .order_by("-created_at")
        .first()
    )


class OptimizeResumeView(APIView):
    def post(self, request, job_id):
        job = get_object_or_404(Job, pk=job_id)
        profile = request.user.profile
        application = _get_application(request.user, job)
        refresh = request.query_params.get("refresh") == "1"

        doc = _cached_doc(application, GeneratedDocument.DocType.TAILORED_RESUME, refresh)
        cached = doc is not None
        if not doc:
            try:
                result = run_resume_optimizer(ProfileSerializer(profile).data, _job_payload(job))
            except AgentError:
                logger.exception("Resume Agent failed")
                return Response(AI_BUSY, status=503)
            doc = GeneratedDocument.objects.create(
                application=application,
                doc_type=GeneratedDocument.DocType.TAILORED_RESUME,
                content=result,
            )

        master = profile.resumes.filter(is_master=True).first()
        return Response(
            {
                "document_id": doc.id,
                "original_ats_score": master.ats_score if master else None,
                "new_ats_score": doc.content.get("new_ats_score"),
                "sections": doc.content.get("sections", {}),
                "ats_improvements": doc.content.get("ats_improvements", []),
                "cached": cached,
            },
            status=200 if cached else 201,
        )


class CoverLetterView(APIView):
    def post(self, request, job_id):
        job = get_object_or_404(Job, pk=job_id)
        profile = request.user.profile
        application = _get_application(request.user, job)
        refresh = request.query_params.get("refresh") == "1"

        doc = _cached_doc(application, GeneratedDocument.DocType.COVER_LETTER, refresh)
        cached = doc is not None
        if not doc:
            try:
                result = run_cover_letter(ProfileSerializer(profile).data, _job_payload(job))
            except AgentError:
                logger.exception("Cover Letter Agent failed")
                return Response(AI_BUSY, status=503)
            doc = GeneratedDocument.objects.create(
                application=application,
                doc_type=GeneratedDocument.DocType.COVER_LETTER,
                content=result,
            )

        return Response(
            {
                "document_id": doc.id,
                "cover_letter": doc.content.get("cover_letter", ""),
                "tone": doc.content.get("tone", ""),
                "cached": cached,
            },
            status=200 if cached else 201,
        )


class InterviewPrepView(APIView):
    def post(self, request, job_id):
        job = get_object_or_404(Job, pk=job_id)
        application = _get_application(request.user, job)
        refresh = request.query_params.get("refresh") == "1"

        doc = _cached_doc(application, GeneratedDocument.DocType.INTERVIEW_PREP, refresh)
        cached = doc is not None
        if not doc:
            try:
                result = run_interview_prep(
                    ProfileSerializer(request.user.profile).data, _job_payload(job)
                )
            except AgentError:
                logger.exception("Interview Agent failed")
                return Response(AI_BUSY, status=503)
            doc = GeneratedDocument.objects.create(
                application=application,
                doc_type=GeneratedDocument.DocType.INTERVIEW_PREP,
                content=result,
            )
        return Response({**doc.content, "cached": cached}, status=200 if cached else 201)


class SkillGapView(APIView):
    def get(self, request, job_id):
        job = get_object_or_404(Job, pk=job_id)
        profile = request.user.profile
        application = _get_application(request.user, job)
        refresh = request.query_params.get("refresh") == "1"

        doc = _cached_doc(application, GeneratedDocument.DocType.SKILL_GAP, refresh)
        if doc:
            return Response({**doc.content, "cached": True})

        # Growth flow: gap analysis needs a match first — run it if absent
        match = MatchResult.objects.filter(profile=profile, job=job).first()
        try:
            if not match:
                result = run_matching(ProfileSerializer(profile).data, _job_payload(job))
                match, _ = MatchResult.objects.update_or_create(
                    profile=profile,
                    job=job,
                    defaults={
                        "fit_score": int(result.get("fit_score", 0)),
                        "reasoning": result.get("reasoning", ""),
                        "matched_skills": result.get("matched_skills", []),
                        "missing_skills": result.get("missing_skills", []),
                    },
                )
            if not match.missing_skills:
                return Response({"gaps": [], "cached": False})
            gap_result = run_skill_gap(
                match.missing_skills,
                {"skills": profile.skills, "experience": profile.experience},
            )
        except AgentError:
            logger.exception("Skill Gap Agent failed")
            return Response(AI_BUSY, status=503)

        doc = GeneratedDocument.objects.create(
            application=application,
            doc_type=GeneratedDocument.DocType.SKILL_GAP,
            content=gap_result,
        )
        return Response({**doc.content, "cached": False}, status=201)


class RoadmapView(APIView):
    def get(self, request):
        profile = request.user.profile
        try:
            result = run_roadmap(ProfileSerializer(profile).data, profile.preferences)
        except AgentError:
            logger.exception("Mentor Agent failed")
            return Response(AI_BUSY, status=503)
        return Response(result)


class DocumentDownloadView(APIView):
    def get(self, request, pk):
        doc = get_object_or_404(
            GeneratedDocument, pk=pk, application__user=request.user
        )
        profile = request.user.profile
        job = doc.application.job
        contact = " | ".join(p for p in [profile.location, profile.phone, request.user.email] if p)

        if doc.doc_type == GeneratedDocument.DocType.TAILORED_RESUME:
            pdf = render_resume_pdf(profile.full_name, contact, doc.content.get("sections", {}))
            filename = f"resume_{job.company}.pdf"
        elif doc.doc_type == GeneratedDocument.DocType.COVER_LETTER:
            pdf = render_cover_letter_pdf(
                profile.full_name, job.title, job.company, doc.content.get("cover_letter", "")
            )
            filename = f"cover_letter_{job.company}.pdf"
        else:
            return Response(
                {"error": {"code": "NOT_PDF", "message": "This document type has no PDF form."}},
                status=400,
            )

        resp = HttpResponse(pdf, content_type="application/pdf")
        resp["Content-Disposition"] = f'attachment; filename="{filename}"'
        return resp
