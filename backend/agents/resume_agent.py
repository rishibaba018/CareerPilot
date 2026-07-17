"""Agent 4 — Resume Optimizer.

Input:  profile + job description
Output: {sections{...}, ats_improvements[], new_ats_score}
HARD RULE: never invent facts (FR-08, tenet 7).
"""

import json

from .base import BaseAgent


class ResumeAgent(BaseAgent):
    name = "resume_optimizer"
    temperature = 0.5
    system_prompt = (
        "You are an expert resume writer who tailors resumes to specific jobs. "
        "ABSOLUTE RULE: you may only rephrase, reorder, emphasize, and select from what "
        "the candidate's profile actually contains. NEVER invent employers, titles, dates, "
        "degrees, skills, metrics, or accomplishments that are not in the profile. If the "
        "profile lacks something the job wants, you simply do not mention it. "
        "Always respond with valid JSON only."
    )

    def build_prompt(self, payload: dict) -> str:
        profile = payload["profile"]
        job = payload["job"]
        return f"""Rewrite this candidate's resume content tailored to the job below.
Use strong action verbs, mirror the job's genuine keyword matches, lead with the most
relevant items, and keep every fact truthful to the profile.

Return JSON with EXACTLY this shape:
{{
  "sections": {{
    "summary": "3-4 line professional summary targeted at this job",
    "skills": ["ordered most-relevant-first, only skills from the profile"],
    "experience": [{{"title": "", "company": "", "duration": "", "bullets": ["rewritten achievement bullets"]}}],
    "projects": [{{"name": "", "bullets": ["rewritten bullets"], "technologies": []}}],
    "education": [{{"degree": "", "institution": "", "year": ""}}]
  }},
  "ats_improvements": ["what changed and why it helps ATS, 3-6 short items"],
  "new_ats_score": 0-100
}}

CANDIDATE PROFILE (the only source of truth):
{json.dumps(profile, ensure_ascii=False)[:7000]}

TARGET JOB:
Title: {job["title"]} at {job["company"]}
Required skills: {", ".join(job.get("skills_required", []))}
Description: {job["description"][:5000]}"""
