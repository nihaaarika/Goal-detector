from __future__ import annotations

import json
import os
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import streamlit as st


# ---------------------------------------------------------------------------
# API Key
# ---------------------------------------------------------------------------

def _get_api_key() -> str:
    try:
        return st.secrets.get("ANTHROPIC_API_KEY", "").strip()
    except Exception:
        return os.environ.get("ANTHROPIC_API_KEY", "").strip()


# ---------------------------------------------------------------------------
# Data model (still needed to load goals.json for context)
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class Goal:
    id: str
    title: str
    theme: str
    timeframe_weeks: int
    difficulty: str
    tags: list[str]
    description: str
    first_steps: list[str]
    resources: list[dict[str, str]]


def load_goals(path: str | Path = "goals.json") -> list[Goal]:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    return [
        Goal(
            id=str(item["id"]),
            title=str(item["title"]),
            theme=str(item.get("theme", "other")),
            timeframe_weeks=int(item.get("timeframe_weeks", 4)),
            difficulty=str(item.get("difficulty", "beginner")),
            tags=[str(t).lower() for t in item.get("tags", [])],
            description=str(item.get("description", "")),
            first_steps=[str(s) for s in item.get("first_steps", [])],
            resources=[dict(r) for r in item.get("resources", [])],
        )
        for item in data.get("goals", [])
    ]


# ---------------------------------------------------------------------------
# Minimal helpers (only what app.py needs, no hardcoded content)
# ---------------------------------------------------------------------------

def normalize_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value.strip()
    if isinstance(value, (list, tuple, set)):
        return " ".join(str(v) for v in value)
    return str(value).strip()


def detect_emotional_signals(responses: dict[str, Any]) -> list[str]:
    """Detect emotional tone from responses — used for UI display only."""
    text = " ".join([
        normalize_text(responses.get("topics")),
        normalize_text(responses.get("long_term_vision")),
        normalize_text(responses.get("family_expectations")),
        normalize_text(responses.get("hard_nos")),
        normalize_text(responses.get("mood")),
    ]).lower()

    signals: list[str] = []
    if any(w in text for w in ["confuse", "lost", "stuck", "uncertain", "not sure", "overwhelm"]):
        signals.append("uncertainty")
    if any(w in text for w in ["pressure", "stressed", "stress", "anxious", "anxiety", "worried"]):
        signals.append("pressure")
    if any(w in text for w in ["excited", "hope", "motivated", "energized", "curious", "interest"]):
        signals.append("curiosity")
    return signals


def recommend_goals(
    goals: list[Goal],
    responses: dict[str, Any],
    top_n: int = 5,
) -> tuple[list[Goal], list[str], float]:
    """
    Stub — themes and scoring are now handled by Claude.
    Returns empty themes so app.py does not crash.
    """
    return goals[:top_n], [], 1.0


# ---------------------------------------------------------------------------
# Claude API — does ALL the work
# ---------------------------------------------------------------------------

_MODEL = "claude-haiku-4-5-20251001"

_SYSTEM_PROMPT = """You are an empathetic, student-friendly AI career and goal discovery assistant.

Rules:
- Use warm, friendly, simple language a student can understand.
- Respect emotional and family context; never judge.
- Be age-appropriate based on age_range if provided.
- Give practical, specific, actionable advice — not generic filler.
- Avoid medical, financial, or legal advice.
- Return ONLY valid JSON. No markdown fences, no explanation, no extra text."""

_OUTPUT_SCHEMA = """{
  "appreciation": "A warm 2-3 sentence message acknowledging the student's specific situation and courage to reflect.",
  "personal_summary": "3-4 sentences summarizing who this student is, what drives them, and what kind of path fits them.",
  "goal_clarity": {
    "primary_goal": "Their clearest immediate goal based on their answers.",
    "secondary_interests": ["other interest 1", "other interest 2"]
  },
  "roadmap": [
    {
      "interest": "Name of the interest area",
      "what_it_means": "Plain-English explanation of what this field actually involves day-to-day.",
      "why_it_suits_you": "Specific reason based on THIS student's answers — not generic.",
      "beginner_steps": ["Step 1", "Step 2", "Step 3", "Step 4"],
      "plan_3_months": [
        "Weeks 1-2: ...",
        "Weeks 3-6: ...",
        "Weeks 7-10: ...",
        "Weeks 11-12: ..."
      ],
      "examples": ["skill or activity 1", "skill or activity 2", "skill or activity 3"]
    }
  ],
  "closing": "A warm 2-sentence closing that speaks to this student's emotional state and encourages them."
}"""


def try_openai_roadmap(
    *,
    responses: dict[str, Any],
    interests: list[str],
    model: str = "",
) -> dict[str, Any] | None:
    """
    Called by app.py. Uses Claude to generate the full roadmap.
    Returns None if API key is missing or call fails.
    """
    api_key = _get_api_key()
    if not api_key:
        st.error("No API key found. Add ANTHROPIC_API_KEY to your Streamlit secrets.")
        return None

    try:
        import anthropic
    except ImportError:
        st.error("`anthropic` package not installed. Run: pip install anthropic")
        return None

    user_message = f"""Here are the student's questionnaire responses:
{json.dumps(responses, indent=2)}

Their selected interests: {', '.join(interests) if interests else 'Not specified'}

Generate a personalized roadmap following this exact JSON structure:
{_OUTPUT_SCHEMA}

Make every field specific to THIS student's answers. Do not use generic filler content."""

    try:
        client = anthropic.Anthropic(api_key=api_key)
        message = client.messages.create(
            model=_MODEL,
            max_tokens=3000,
            system=_SYSTEM_PROMPT,
            messages=[{"role": "user", "content": user_message}],
        )

        raw = message.content[0].text.strip() if message.content else ""
        if not raw:
            return None

        # Strip markdown fences if model adds them
        raw = re.sub(r"^```(?:json)?\s*", "", raw)
        raw = re.sub(r"\s*```$", "", raw)

        parsed = json.loads(raw)
        return parsed if isinstance(parsed, dict) else None

    except json.JSONDecodeError:
        st.error("Claude returned invalid JSON. Try again.")
        return None
    except Exception as e:
        st.error(f"Claude API error: {e}")
        return None


# ---------------------------------------------------------------------------
# These are called by app.py — now delegated to Claude output
# ---------------------------------------------------------------------------

def appreciation_message(responses: dict[str, Any], signals: list[str]) -> str:
    """Fallback only — Claude generates this in try_openai_roadmap."""
    return ""


def supportive_closing(responses: dict[str, Any], signals: list[str]) -> str:
    """Fallback only — Claude generates this in try_openai_roadmap."""
    return ""


def build_interest_roadmap(
    *,
    interest: str,
    responses: dict[str, Any],
    all_goals: list[Goal],
) -> dict[str, Any]:
    """Fallback only — Claude generates the full roadmap in try_openai_roadmap."""
    return {
        "interest": interest,
        "meaning": "",
        "why": "",
        "next_steps": [],
        "plan_3_months": [],
        "example_skills": [],
        "recommended_goals": [],
    }