"""Agent 5 — Cover Letter Agent.

Input:  profile + job + company
Output: {cover_letter, tone}
"""

import json

from .base import BaseAgent


class CoverLetterAgent(BaseAgent):
    name = "cover_letter"
    temperature = 0.7
    system_prompt = (
        "You write compelling, specific, human-sounding cover letters. "
        "No clichés ('I am writing to express...'), no flattery padding, no invented "
        "facts — only experiences and skills actually present in the candidate profile. "
        "Always respond with valid JSON only."
    )

    def build_prompt(self, payload: dict) -> str:
        profile = payload["profile"]
        job = payload["job"]
        return f"""Write a cover letter (250-350 words) from this candidate for this job.
Structure: a hook tying the candidate's strongest relevant achievement to the company's
work, one paragraph mapping 2-3 concrete experiences to the job's needs, a confident
close. Use the candidate's real name. Plain text with paragraph breaks (\\n\\n).

Return JSON with EXACTLY this shape:
{{"cover_letter": "the letter text", "tone": "one word, e.g. confident/warm/direct"}}

CANDIDATE PROFILE (only source of truth):
{json.dumps(profile, ensure_ascii=False)[:6000]}

JOB:
Title: {job["title"]} at {job["company"]}
Description: {job["description"][:4000]}"""
