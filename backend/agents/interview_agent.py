"""Agent 7 — Interview Prep Agent.

Input:  job description + profile
Output: {technical[], hr[], questions_about_projects[]}
"""

import json

from .base import BaseAgent


class InterviewAgent(BaseAgent):
    name = "interview"
    temperature = 0.6
    system_prompt = (
        "You are a senior interviewer preparing a candidate for a specific job. Questions "
        "must be specific to THIS job's stack and THIS candidate's actual background — "
        "no generic filler. Each question gets a short 'hint' on what a strong answer covers. "
        "Always respond with valid JSON only."
    )

    def build_prompt(self, payload: dict) -> str:
        job = payload["job"]
        return f"""Generate likely interview questions for this candidate applying to this job.

Return JSON with EXACTLY this shape:
{{
  "technical": [{{"question": "", "hint": "what a strong answer covers"}}],
  "hr": [{{"question": "", "hint": ""}}],
  "questions_about_projects": [{{"question": "", "hint": ""}}]
}}
Provide 5 technical, 3 hr, and 3 project questions (project ones must reference the
candidate's real projects/experience by name).

JOB:
Title: {job["title"]} at {job["company"]}
Description: {job["description"][:4000]}

CANDIDATE PROFILE:
{json.dumps(payload["profile"], ensure_ascii=False)[:5000]}"""
