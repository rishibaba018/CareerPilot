"""Agent 9 — Career Mentor Agent.

Input:  profile + preferences (goals)
Output: {roadmap: [{phase, skills, certifications, target_roles}]}
"""

import json

from .base import BaseAgent


class MentorAgent(BaseAgent):
    name = "mentor"
    temperature = 0.5
    system_prompt = (
        "You are a candid career mentor for software professionals. You build 2-year "
        "roadmaps grounded in the candidate's real current level — no fantasy jumps. "
        "Always respond with valid JSON only."
    )

    def build_prompt(self, payload: dict) -> str:
        return f"""Build a 2-year career roadmap for this candidate toward their target role.

Return JSON with EXACTLY this shape:
{{"roadmap": [{{"phase": "e.g. Months 0-6", "focus": "one-line theme", "skills": [""], "certifications": [""], "target_roles": [""]}}]}}
Use 3-4 phases. Certifications only where they genuinely matter (cloud, etc.) — empty list otherwise.

CANDIDATE PROFILE:
{json.dumps(payload["profile"], ensure_ascii=False)[:5000]}

STATED PREFERENCES / GOALS:
{json.dumps(payload["preferences"], ensure_ascii=False)[:1000]}"""
