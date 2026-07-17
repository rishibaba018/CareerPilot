"""Agent orchestrator — decides which agents run and in what order.

Flows (from master-plan §12), added sprint by sprint:
- Onboarding: resume upload -> ProfileAgent -> save profile -> ATS score  [live]
- Discovery:  preferences -> DiscoveryAgent -> MatchingAgent on top results
- Apply:      ResumeAgent + CoverLetterAgent -> user review
- Growth:     SkillGapAgent -> MentorAgent
"""

from .discovery_agent import DiscoveryAgent
from .matching_agent import MatchingAgent
from .profile_agent import ProfileAgent


def run_onboarding(resume_text: str) -> dict:
    """Onboarding flow: parse the resume and score ATS-friendliness."""
    return ProfileAgent().run({"resume_text": resume_text})


def run_discovery(preferences: dict) -> dict:
    """Discovery flow: fetch/refresh the job pool for the user's preferences."""
    return DiscoveryAgent().run({"preferences": preferences})


def run_matching(profile: dict, job: dict) -> dict:
    """Matching flow: score profile-vs-job fit with reasoning."""
    return MatchingAgent().run({"profile": profile, "job": job})
