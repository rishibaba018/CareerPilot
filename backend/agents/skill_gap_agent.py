"""Agent 6 — Skill Gap Agent.

Input:  missing_skills (from Matching Agent) + profile context
Output: {gaps: [{skill, priority, resource, weeks}]}
"""

import json

from .base import BaseAgent


class SkillGapAgent(BaseAgent):
    name = "skill_gap"
    temperature = 0.4
    system_prompt = (
        "You are a pragmatic learning advisor for software careers. You turn skill gaps "
        "into short, realistic learning plans with one specific, well-known free or cheap "
        "resource per skill (official docs, freeCodeCamp, CS50, well-known courses). "
        "Always respond with valid JSON only."
    )

    def build_prompt(self, payload: dict) -> str:
        return f"""The candidate below is missing these skills for a target job:
{json.dumps(payload["missing_skills"])}

Candidate context (current skills and background):
{json.dumps(payload["profile_context"], ensure_ascii=False)[:3000]}

For each missing skill, estimate how long it takes THIS candidate to reach
job-ready basics given what they already know.

Return JSON with EXACTLY this shape:
{{"gaps": [{{"skill": "", "priority": "high|medium|low", "resource": "one specific course/doc name", "weeks": 1}}]}}"""
