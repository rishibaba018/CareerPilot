# CareerPilot — AI-Powered Intelligent Job Application Assistant

## What this project is
An autonomous AI career copilot for a 24-hour hackathon. Full details, architecture,
database schema, API design, and sprint plan are in `/docs/master-plan.md` and
`/docs/srs-lite.md` — READ THOSE FIRST before writing any code.

## Tech stack (do not deviate without asking)
- Frontend: React + Vite + Tailwind CSS + ShadCN UI
- Backend: Django + Django REST Framework
- Database: PostgreSQL (Neon in production, local Postgres or SQLite for dev)
- Auth: JWT (djangorestframework-simplejwt)
- AI: Gemini API, called through a single `BaseAgent` class in `backend/agents/`
- Jobs data: JSearch or Adzuna API, with a seeded fallback of ~50 real jobs

## Repo layout
```
careerpilot/
├── docs/                # master plan, SRS, this file
├── frontend/             # React + Vite app
└── backend/              # Django project
    ├── config/
    ├── accounts/
    ├── profiles/
    ├── resumes/
    ├── jobs/
    ├── matching/
    ├── applications/
    ├── agents/           # BaseAgent + 9 specialist agents + orchestrator
    └── documents/
```

## Engineering tenets (use these to break ties)
1. Reliability over Features
2. Speed over Perfection
3. User Experience over Technical Elegance
4. Reuse over Reinvention — use proven libraries, don't hand-roll auth/PDF/etc.
5. Simplicity over Flexibility — one backend, no microservices, no task queues
6. Security over Convenience — secrets ALWAYS in `.env`, never hardcoded
7. Honesty over Hype — clearly label simulated features (e.g. application submission)

## Working agreement for autonomous sessions
- Work sprint by sprint, in the order defined in `/docs/master-plan.md` section 13.
- After finishing a sprint's tasks: run the app, fix errors yourself, then write a
  short summary of what was built and what's left, and commit with a clear message.
- Do NOT invent scope beyond what's in the docs. If something is ambiguous, make the
  most reasonable choice consistent with the tenets above and note the assumption in
  your summary rather than stopping to ask.
- Never commit real API keys. Use `.env.example` with placeholder values.
- Keep the AI agent prompts truthful: resume/cover-letter generation must never
  invent experience, skills, or qualifications the user didn't provide.
- Prefer small, testable commits over one giant commit per sprint.

## Current sprint
See `/docs/master-plan.md` §13. Start at Sprint 0 unless told otherwise.
