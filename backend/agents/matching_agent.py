"""Agent 3 — Matching Agent.

Input:  profile + job description
Output: {fit_score, reasoning, matched_skills[], missing_skills[]}
"""

import json

from .base import BaseAgent


class MatchingAgent(BaseAgent):
    name = "matching"
    temperature = 0.2
    system_prompt = (
        "You are a technical recruiter who scores candidate-job fit with brutal honesty "
        "and explains scores in plain language a candidate can act on. "
        "Base your judgment ONLY on the profile provided — never assume unstated skills. "
        "Always respond with valid JSON only."
    )

    def build_prompt(self, payload: dict) -> str:
        profile = payload["profile"]
        job = payload["job"]
        return f"""Score how well this candidate fits this job.

Return JSON with EXACTLY this shape:
{{
  "fit_score": 0-100,
  "reasoning": "3-5 sentences: why this score, naming the specific overlaps and gaps",
  "matched_skills": ["skills the candidate has that the job wants"],
  "missing_skills": ["skills the job wants that the candidate lacks"]
}}

Scoring guide: 85+ near-perfect overlap incl. experience level; 70-84 strong fit with
minor gaps; 50-69 partial fit, real gaps; below 50 weak fit. Consider skills overlap
(weight ~50%), experience relevance (~30%), education/level match (~20%).

CANDIDATE PROFILE:
{json.dumps(profile, ensure_ascii=False)[:6000]}

JOB:
Title: {job["title"]} at {job["company"]}
Required skills: {", ".join(job.get("skills_required", []))}
Description: {job["description"][:6000]}"""
