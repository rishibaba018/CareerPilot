"""Agent 8 — Tracking Agent.

Input:  the user's applications (status, ages, fit scores)
Output: {insights[], suggestions[]}
"""

import json

from .base import BaseAgent


class TrackingAgent(BaseAgent):
    name = "tracking"
    temperature = 0.4
    system_prompt = (
        "You are a job-search coach reviewing a candidate's application pipeline. "
        "You spot honest patterns (stalled applications, low-fit targeting, no follow-ups, "
        "good momentum) and give specific, kind but direct advice. "
        "Always respond with valid JSON only."
    )

    def build_prompt(self, payload: dict) -> str:
        return f"""Review this application pipeline and give the candidate insights.

Return JSON with EXACTLY this shape:
{{
  "insights": ["2-4 short observations about their pipeline patterns"],
  "suggestions": ["2-3 specific next actions, each doable this week"]
}}

APPLICATIONS (status, days in that status, job, fit score):
{json.dumps(payload["applications"], ensure_ascii=False)[:5000]}

Today's context: preferences = {json.dumps(payload.get("preferences", {}))[:500]}"""
