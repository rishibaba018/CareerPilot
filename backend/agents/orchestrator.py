"""Agent orchestrator — decides which agents run and in what order.

Flows (from master-plan §12) are added sprint by sprint:
- Onboarding: resume upload -> ProfileAgent -> save profile -> ATS score
- Discovery:  preferences -> DiscoveryAgent -> MatchingAgent on top results
- Apply:      ResumeAgent + CoverLetterAgent -> user review
- Growth:     SkillGapAgent -> MentorAgent
"""
