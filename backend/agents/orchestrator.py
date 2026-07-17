"""Agent orchestrator — decides which agents run and in what order.

Flows (from master-plan §12), added sprint by sprint:
- Onboarding: resume upload -> ProfileAgent -> save profile -> ATS score  [live]
- Discovery:  preferences -> DiscoveryAgent -> MatchingAgent on top results
- Apply:      ResumeAgent + CoverLetterAgent -> user review
- Growth:     SkillGapAgent -> MentorAgent
"""

from .cover_letter_agent import CoverLetterAgent
from .discovery_agent import DiscoveryAgent
from .interview_agent import InterviewAgent
from .matching_agent import MatchingAgent
from .mentor_agent import MentorAgent
from .profile_agent import ProfileAgent
from .resume_agent import ResumeAgent
from .skill_gap_agent import SkillGapAgent


def run_onboarding(resume_text: str) -> dict:
    """Onboarding flow: parse the resume and score ATS-friendliness."""
    return ProfileAgent().run({"resume_text": resume_text})


def run_discovery(preferences: dict) -> dict:
    """Discovery flow: fetch/refresh the job pool for the user's preferences."""
    return DiscoveryAgent().run({"preferences": preferences})


def run_matching(profile: dict, job: dict) -> dict:
    """Matching flow: score profile-vs-job fit with reasoning."""
    return MatchingAgent().run({"profile": profile, "job": job})


def run_resume_optimizer(profile: dict, job: dict) -> dict:
    """Apply flow: tailor the resume to a specific job (truthfully)."""
    return ResumeAgent().run({"profile": profile, "job": job})


def run_cover_letter(profile: dict, job: dict) -> dict:
    """Apply flow: write a personalized cover letter."""
    return CoverLetterAgent().run({"profile": profile, "job": job})


def run_skill_gap(missing_skills: list, profile_context: dict) -> dict:
    """Growth flow step 1: turn missing skills into a learning plan."""
    return SkillGapAgent().run(
        {"missing_skills": missing_skills, "profile_context": profile_context}
    )


def run_interview_prep(profile: dict, job: dict) -> dict:
    """Prep flow: job-specific interview question bank."""
    return InterviewAgent().run({"profile": profile, "job": job})


def run_roadmap(profile: dict, preferences: dict) -> dict:
    """Growth flow step 2: 2-year career roadmap."""
    return MentorAgent().run({"profile": profile, "preferences": preferences})
