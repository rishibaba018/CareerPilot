"""Seed the fallback job pool (master-plan §12: if the jobs API dies, the app still shines).

Idempotent: jobs are keyed by external_id, re-running updates in place.
"""

from django.core.management.base import BaseCommand
from django.utils import timezone

from jobs.models import Job

SEED_JOBS = [
    {
        "title": "Backend Developer (Python/Django)",
        "company": "Finlytica",
        "location": "Hyderabad, India",
        "work_mode": "hybrid",
        "salary_range": "₹6-10 LPA",
        "skills_required": ["Python", "Django", "PostgreSQL", "REST APIs", "Git", "Docker"],
        "description": "Finlytica builds analytics dashboards for mid-size lenders. You will design and ship Django REST APIs powering our reporting suite, own PostgreSQL schema changes, and harden endpoints used by 40k monthly users. We expect solid Python fundamentals, experience with DRF or similar, and comfort writing tests. Nice to have: Docker, Redis caching, and CI pipelines. You'll pair weekly with senior engineers and own one product area end to end within your first quarter.",
    },
    {
        "title": "Frontend Engineer (React)",
        "company": "Cartloop Commerce",
        "location": "Bangalore, India",
        "work_mode": "remote",
        "salary_range": "₹8-14 LPA",
        "skills_required": ["React", "TypeScript", "Tailwind CSS", "REST APIs", "Testing Library"],
        "description": "Cartloop powers storefronts for 900+ D2C brands. We need a React engineer to build checkout and merchandising surfaces in TypeScript, with a strong eye for performance (LCP budgets, code-splitting) and accessibility. You'll work with designers in Figma, ship behind feature flags, and measure everything. Experience with React Query/Redux, Vite, and component testing is valued. Fully remote within India, quarterly meetups.",
    },
    {
        "title": "Full-Stack Developer",
        "company": "MedBridge Health",
        "location": "Pune, India",
        "work_mode": "onsite",
        "salary_range": "₹7-12 LPA",
        "skills_required": ["Python", "Django", "React", "PostgreSQL", "AWS"],
        "description": "MedBridge digitizes clinic workflows for 300+ hospitals. As a full-stack developer you'll build patient-intake and scheduling features across a Django backend and React frontend, integrate with lab systems over HL7/REST, and deploy to AWS ECS. We value engineers who write clear code, add tests without being asked, and can talk to clinicians about requirements. 2+ years experience or an exceptional project portfolio required.",
    },
    {
        "title": "Data Analyst",
        "company": "UrbanKart",
        "location": "Gurgaon, India",
        "work_mode": "hybrid",
        "salary_range": "₹5-9 LPA",
        "skills_required": ["SQL", "Python", "Pandas", "Power BI", "Statistics"],
        "description": "UrbanKart's growth team needs a data analyst to own funnel and retention reporting. You'll write production SQL against Snowflake, build Pandas pipelines for cohort analysis, and ship Power BI dashboards executives actually use. Strong statistics fundamentals (significance testing, regression) required; dbt and Airflow exposure is a plus. You'll present weekly insights directly to the VP Growth.",
    },
    {
        "title": "Machine Learning Engineer",
        "company": "Veriscan AI",
        "location": "Bangalore, India",
        "work_mode": "hybrid",
        "salary_range": "₹12-20 LPA",
        "skills_required": ["Python", "PyTorch", "scikit-learn", "MLOps", "Docker", "AWS"],
        "description": "Veriscan builds document-fraud detection for fintechs. You'll train and deploy vision/NLP models that process 2M documents monthly, own the feature store and evaluation harness, and reduce false-positive rates for enterprise clients. Production ML experience (serving, monitoring, drift) matters more to us than papers. Stack: PyTorch, FastAPI, SageMaker, Docker.",
    },
    {
        "title": "DevOps Engineer",
        "company": "Skyrail Systems",
        "location": "Chennai, India",
        "work_mode": "onsite",
        "salary_range": "₹9-15 LPA",
        "skills_required": ["Linux", "Docker", "Kubernetes", "Terraform", "CI/CD", "AWS"],
        "description": "Skyrail runs logistics infrastructure for rail freight operators. You'll own our EKS clusters, Terraform modules, and GitHub Actions pipelines; drive down deploy times; and build observability with Prometheus/Grafana. On-call one week in six with real compensation. We want someone who automates ruthlessly and documents as they go.",
    },
    {
        "title": "Junior Software Engineer",
        "company": "Nexbyte Labs",
        "location": "Hyderabad, India",
        "work_mode": "onsite",
        "salary_range": "₹4-6 LPA",
        "skills_required": ["Python", "JavaScript", "SQL", "Git"],
        "description": "Nexbyte is a 40-person services firm building web apps for US startups. This new-grad role rotates you through two client projects a year with a dedicated mentor. You'll fix bugs in week one, own small features by month two, and learn professional Git workflow, code review, and testing discipline. We hire for fundamentals and curiosity over specific frameworks. 2025/2026 graduates welcome.",
    },
    {
        "title": "React Native Developer",
        "company": "FitOrbit",
        "location": "Remote, India",
        "work_mode": "remote",
        "salary_range": "₹8-13 LPA",
        "skills_required": ["React Native", "TypeScript", "REST APIs", "Redux", "App Store deployment"],
        "description": "FitOrbit's fitness app has 500k installs across iOS and Android. You'll ship workout-tracking and social features in React Native + TypeScript, improve cold-start time, and own releases to both stores. Experience with native modules, push notifications, and offline-first sync is a strong plus. Small team, high ownership, async-first culture.",
    },
    {
        "title": "QA Automation Engineer",
        "company": "Payhive",
        "location": "Mumbai, India",
        "work_mode": "hybrid",
        "salary_range": "₹6-10 LPA",
        "skills_required": ["Python", "Selenium", "Playwright", "API testing", "CI/CD"],
        "description": "Payhive processes payroll for 2,000 SMBs, so regressions cost real money. You'll build our Playwright end-to-end suite from 40% to 90% critical-path coverage, own API test harnesses in pytest, and gate releases in CI. We want an engineer who treats test code as production code and can push back on flaky-test culture.",
    },
    {
        "title": "Backend Engineer (Node.js)",
        "company": "Streamline Media",
        "location": "Bangalore, India",
        "work_mode": "remote",
        "salary_range": "₹10-16 LPA",
        "skills_required": ["Node.js", "TypeScript", "MongoDB", "Redis", "Microservices"],
        "description": "Streamline delivers video APIs to broadcasters. You'll build ingestion and playback services in Node/TypeScript handling 10k req/s, tune MongoDB and Redis, and design for graceful degradation. Deep async/streams knowledge and production debugging stories matter here. Kafka and WebRTC experience are pluses.",
    },
    {
        "title": "Data Engineer",
        "company": "AgriSense",
        "location": "Pune, India",
        "work_mode": "hybrid",
        "salary_range": "₹9-14 LPA",
        "skills_required": ["Python", "SQL", "Airflow", "Spark", "AWS", "dbt"],
        "description": "AgriSense aggregates satellite and sensor data for crop insurers. You'll build Airflow/Spark pipelines processing 3TB weekly, model warehouse tables in dbt, and keep data SLAs for ML teams downstream. Strong SQL and one production pipeline war story required. Bonus: geospatial data experience (PostGIS, rasterio).",
    },
    {
        "title": "Software Engineer - Platform",
        "company": "Kite Financial",
        "location": "Bangalore, India",
        "work_mode": "onsite",
        "salary_range": "₹15-25 LPA",
        "skills_required": ["Go", "Python", "Kubernetes", "gRPC", "PostgreSQL"],
        "description": "Kite's platform team builds the paved road other engineers ship on: service templates, deploy tooling, golden-path CI. You'll write Go services, maintain internal gRPC APIs, and cut service-bootstrap time from days to minutes. Strong CS fundamentals and empathy for developer experience required; fintech background not necessary.",
    },
    {
        "title": "Python Developer (Automation)",
        "company": "Clearstack BPO",
        "location": "Hyderabad, India",
        "work_mode": "onsite",
        "salary_range": "₹5-8 LPA",
        "skills_required": ["Python", "Pandas", "Selenium", "REST APIs", "Excel automation"],
        "description": "Clearstack automates back-office workflows for insurance clients. You'll replace manual Excel processes with Python (Pandas, openpyxl), build scrapers and API integrations, and productionize scripts with logging, retries, and alerts. Great first or second job for someone who loves making tedious things disappear.",
    },
    {
        "title": "Frontend Developer (Vue.js)",
        "company": "Hotelio",
        "location": "Goa, India",
        "work_mode": "onsite",
        "salary_range": "₹6-9 LPA",
        "skills_required": ["Vue.js", "JavaScript", "CSS", "REST APIs", "Vite"],
        "description": "Hotelio builds property-management software for boutique hotels. You'll own our booking-calendar UI in Vue 3, improve mobile responsiveness for front-desk tablets, and work directly with hotel operators for feedback. React experience transfers fine — we care about component thinking and CSS craft. Yes, the office is in Goa.",
    },
    {
        "title": "Site Reliability Engineer",
        "company": "Torrentz Cloud",
        "location": "Remote, India",
        "work_mode": "remote",
        "salary_range": "₹14-22 LPA",
        "skills_required": ["Linux", "Kubernetes", "Prometheus", "Python", "Incident response", "Networking"],
        "description": "Torrentz hosts managed databases for 1,200 customers. As an SRE you'll own SLOs, run blameless postmortems, automate failover runbooks in Python, and reduce page volume (currently ~4/week per engineer, target 1). Deep Linux and networking knowledge required. We fund conference talks about what you build.",
    },
    {
        "title": "Associate Product Engineer",
        "company": "EduSpark",
        "location": "Delhi, India",
        "work_mode": "hybrid",
        "salary_range": "₹4.5-7 LPA",
        "skills_required": ["JavaScript", "React", "Node.js", "SQL"],
        "description": "EduSpark builds test-prep tools used by 200k students. This early-career role spans the stack: React quiz interfaces, Node APIs, and analytics queries. You'll ship weekly, demo to the team on Fridays, and talk to students monthly. We've promoted our last three associates within 18 months. Freshers with strong projects encouraged to apply.",
    },
    {
        "title": "Django Developer",
        "company": "LegalDocs Pro",
        "location": "Mumbai, India",
        "work_mode": "hybrid",
        "salary_range": "₹7-11 LPA",
        "skills_required": ["Python", "Django", "Celery", "PostgreSQL", "Redis", "REST APIs"],
        "description": "LegalDocs automates contract drafting for law firms. You'll extend our Django monolith (yes, proudly a monolith), build document-generation pipelines with Celery, and design multi-tenant data isolation. We want someone who knows Django deeply — ORM query optimization, migrations at scale, and the admin's hidden powers.",
    },
    {
        "title": "Cloud Engineer (Azure)",
        "company": "Meridian Consulting",
        "location": "Noida, India",
        "work_mode": "onsite",
        "salary_range": "₹8-13 LPA",
        "skills_required": ["Azure", "Terraform", "PowerShell", "Networking", "CI/CD"],
        "description": "Meridian migrates enterprise workloads to Azure. You'll design landing zones, write Terraform and Bicep modules, and run migration cutovers for banking clients. AZ-104/305 certifications sponsored. Strong networking fundamentals (VNets, ExpressRoute, DNS) required; client-facing communication skills essential.",
    },
    {
        "title": "AI Application Developer",
        "company": "Brightloop",
        "location": "Bangalore, India",
        "work_mode": "remote",
        "salary_range": "₹10-18 LPA",
        "skills_required": ["Python", "LLM APIs", "FastAPI", "Prompt engineering", "Vector databases", "React"],
        "description": "Brightloop ships AI copilots for customer-support teams. You'll build LLM-powered features end to end: retrieval pipelines over customer knowledge bases, agent orchestration with tool use, evaluation harnesses, and the React surfaces users touch. You should have shipped at least one real LLM feature (not a demo) and have opinions about latency, cost, and hallucination guardrails.",
    },
    {
        "title": "Embedded Software Engineer",
        "company": "VoltEdge Mobility",
        "location": "Chennai, India",
        "work_mode": "onsite",
        "salary_range": "₹8-14 LPA",
        "skills_required": ["C", "C++", "RTOS", "CAN bus", "Python"],
        "description": "VoltEdge builds battery-management systems for electric two-wheelers. You'll write firmware in C/C++ on FreeRTOS, implement CAN diagnostics, and build Python test rigs for hardware-in-loop validation. Automotive experience helps but strong embedded fundamentals (interrupts, memory, debugging with a scope) matter most.",
    },
]


class Command(BaseCommand):
    help = "Seed the fallback job pool (idempotent)."

    def handle(self, *args, **options):
        created = 0
        for i, data in enumerate(SEED_JOBS):
            _, was_created = Job.objects.update_or_create(
                external_id=f"seed-{i + 1}",
                defaults={**data, "url": "", "posted_at": timezone.now()},
            )
            created += int(was_created)
        self.stdout.write(f"Seeded jobs: {created} new, {len(SEED_JOBS) - created} updated.")
