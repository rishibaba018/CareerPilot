"""Agent orchestrator — decides which agents run and in what order.

Flows (from master-plan §12), added sprint by sprint:
- Onboarding: resume upload -> ProfileAgent -> save profile -> ATS score  [live]
- Discovery:  preferences -> DiscoveryAgent -> MatchingAgent on top results
- Apply:      ResumeAgent + CoverLetterAgent -> user review
- Growth:     SkillGapAgent -> MentorAgent
"""

from .profile_agent import ProfileAgent


def run_onboarding(resume_text: str) -> dict:
    """Onboarding flow: parse the resume and score ATS-friendliness."""
    return ProfileAgent().run({"resume_text": resume_text})
