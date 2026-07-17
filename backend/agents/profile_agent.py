"""Agent 1 — Profile Agent.

Input:  raw resume text
Output: {skills[], education[], experience[], projects[], summary,
         ats_score, ats_feedback[]}
"""

from .base import BaseAgent


class ProfileAgent(BaseAgent):
    name = "profile"
    temperature = 0.2
    system_prompt = (
        "You are an expert resume parser and ATS (Applicant Tracking System) analyst. "
        "You extract structured data from resume text with total accuracy. "
        "CRITICAL RULE: only extract information that is actually present in the resume. "
        "Never invent, embellish, or infer skills, employers, degrees, dates, or projects "
        "that are not explicitly written. If a field is absent, return an empty list or "
        "empty string for it. Always respond with valid JSON only."
    )

    def build_prompt(self, payload: dict) -> str:
        resume_text = payload["resume_text"]
        return f"""Parse the resume below and score its ATS-friendliness.

Return JSON with EXACTLY this shape:
{{
  "full_name": "string, or empty if not found",
  "phone": "string, or empty",
  "location": "string, or empty",
  "summary": "2-3 sentence professional summary based only on what the resume says",
  "skills": ["skill1", "skill2"],
  "education": [{{"degree": "", "institution": "", "year": ""}}],
  "experience": [{{"title": "", "company": "", "duration": "", "description": ""}}],
  "projects": [{{"name": "", "description": "", "technologies": []}}],
  "ats_score": 0,
  "ats_feedback": ["short actionable improvement tips"]
}}

ATS scoring rubric (0-100): contact info present (10), clear section headings (15),
quantified achievements (20), relevant keywords/skills listed (25), consistent
formatting inferred from text (15), no large unreadable gaps (15). Be honest and
slightly strict; most resumes score 55-80.

RESUME TEXT:
---
{resume_text[:15000]}
---"""
