"""BaseAgent — the single gateway to Gemini for all 9 specialist agents.

Every agent subclasses this with its own `name`, `system_prompt`, and
`build_prompt(payload)`. `run()` handles the Gemini call, JSON parsing
(including ```json fences), and one retry on failure.
"""

import json
import logging

from django.conf import settings

logger = logging.getLogger(__name__)


class AgentError(Exception):
    """Raised when an agent cannot produce a valid result after retrying."""


class BaseAgent:
    name = "base"
    system_prompt = "You are a helpful assistant. Always respond with valid JSON."
    temperature = 0.4  # low for scoring agents; writing agents override higher

    def build_prompt(self, payload: dict) -> str:
        raise NotImplementedError

    def run(self, payload: dict) -> dict:
        prompt = self.build_prompt(payload)
        last_error = None
        for attempt in range(2):
            try:
                raw = self._call_gemini(prompt)
                return self._parse_json(raw)
            except Exception as exc:  # noqa: BLE001 — retry any Gemini/parse failure once
                last_error = exc
                logger.warning("Agent %s attempt %d failed: %s", self.name, attempt + 1, exc)
        raise AgentError(f"Agent '{self.name}' failed after retry: {last_error}")

    def _call_gemini(self, prompt: str) -> str:
        if not settings.GEMINI_API_KEY:
            raise AgentError("GEMINI_API_KEY is not configured")
        from google import genai
        from google.genai import types

        client = genai.Client(api_key=settings.GEMINI_API_KEY)
        response = client.models.generate_content(
            model=settings.GEMINI_MODEL,
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=self.system_prompt,
                temperature=self.temperature,
                response_mime_type="application/json",
            ),
        )
        return response.text or ""

    @staticmethod
    def _parse_json(raw: str) -> dict:
        text = raw.strip()
        if text.startswith("```"):
            text = text.split("```")[1]
            text = text.removeprefix("json").strip()
        return json.loads(text)
