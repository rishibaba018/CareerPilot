"""Agent 2 — Job Discovery Agent.

Calls the JSearch API (RapidAPI) when a key is configured and upserts
normalized jobs. Without a key, discovery silently falls back to the
seeded job pool (master-plan §12/§19).
"""

import logging

import requests
from django.conf import settings
from django.core.management import call_command
from django.utils.dateparse import parse_datetime

from jobs.models import Job

logger = logging.getLogger(__name__)

JSEARCH_URL = "https://jsearch.p.rapidapi.com/search"


class DiscoveryAgent:
    name = "discovery"

    def run(self, payload: dict) -> dict:
        prefs = payload.get("preferences") or {}
        role = prefs.get("role") or "software developer"
        locations = prefs.get("locations") or []
        query = f"{role} in {locations[0]}" if locations else role

        added = 0
        source = "seeded"
        if settings.JSEARCH_API_KEY:
            try:
                added = self._fetch_jsearch(query)
                source = "jsearch"
            except Exception as exc:  # noqa: BLE001 — API failure must never break discovery
                logger.warning("JSearch failed, using seeded pool: %s", exc)

        if Job.objects.count() == 0:
            call_command("seed_jobs")

        return {"source": source, "jobs_added": added, "total_jobs": Job.objects.count()}

    def _fetch_jsearch(self, query: str) -> int:
        resp = requests.get(
            JSEARCH_URL,
            headers={
                "X-RapidAPI-Key": settings.JSEARCH_API_KEY,
                "X-RapidAPI-Host": "jsearch.p.rapidapi.com",
            },
            params={"query": query, "num_pages": 1},
            timeout=20,
        )
        resp.raise_for_status()
        added = 0
        for item in resp.json().get("data", []):
            external_id = item.get("job_id")
            if not external_id:
                continue
            _, created = Job.objects.update_or_create(
                external_id=external_id,
                defaults={
                    "title": (item.get("job_title") or "")[:255],
                    "company": (item.get("employer_name") or "")[:255],
                    "location": ", ".join(
                        p for p in [item.get("job_city"), item.get("job_country")] if p
                    )[:255],
                    "description": item.get("job_description") or "",
                    "skills_required": (item.get("job_highlights") or {}).get("Qualifications", [])[:15],
                    "work_mode": "remote" if item.get("job_is_remote") else "",
                    "url": (item.get("job_apply_link") or "")[:500],
                    "posted_at": parse_datetime(item.get("job_posted_at_datetime_utc") or "") or None,
                },
            )
            added += int(created)
        return added
