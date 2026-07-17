"""Refine Agent — conversational editor for generated documents.

Takes the current tailored resume (or cover letter), plus a user instruction
("make the summary punchier", "reorder skills for backend", "make the accent
color green"), and returns the full updated document + a short reply.
"""

import json

from .base import BaseAgent


class RefineAgent(BaseAgent):
    name = "refine"
    temperature = 0.5
    system_prompt = (
        "You are an interactive resume/cover-letter editor. You apply the user's "
        "instruction to the current document and return the COMPLETE updated document. "
        "ABSOLUTE RULES: never invent employers, dates, degrees, skills, or metrics not "
        "already present in the document or profile; keep everything truthful. If the "
        "instruction asks for a visual/style change (colors, tone of styling), set "
        "style.accent to an appropriate hex color. If an instruction cannot be done "
        "truthfully (e.g. 'add 5 years at Google'), refuse it in `reply` and return the "
        "document unchanged. Always respond with valid JSON only."
    )

    def build_prompt(self, payload: dict) -> str:
        doc_type = payload["doc_type"]
        if doc_type == "resume":
            shape = (
                '{"sections": {"summary": "", "skills": [], '
                '"experience": [{"title": "", "company": "", "duration": "", "bullets": []}], '
                '"projects": [{"name": "", "bullets": [], "technologies": []}], '
                '"education": [{"degree": "", "institution": "", "year": ""}]}, '
                '"style": {"accent": "#3b4bd8"}, '
                '"reply": "1-2 sentences: what you changed"}'
            )
            current = json.dumps(
                {"sections": payload["current"], "style": payload.get("style") or {}},
                ensure_ascii=False,
            )
        else:
            shape = (
                '{"cover_letter": "full letter text", "tone": "one word", '
                '"style": {"accent": "#3b4bd8"}, '
                '"reply": "1-2 sentences: what you changed"}'
            )
            current = json.dumps(
                {"cover_letter": payload["current"], "style": payload.get("style") or {}},
                ensure_ascii=False,
            )

        return f"""Apply the user's instruction to this {doc_type} (for the job: {payload["job_title"]} at {payload["company"]}).

Return JSON with EXACTLY this shape (the FULL updated document, not a diff):
{shape}

CURRENT DOCUMENT:
{current[:8000]}

USER INSTRUCTION:
{payload["instruction"][:1000]}"""
