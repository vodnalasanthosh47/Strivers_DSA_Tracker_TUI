"""Load questions.json and merge with progress.json."""
from __future__ import annotations

import json
from pathlib import Path

from data.store import load_progress, ensure_data_dir

QUESTIONS_FILE = Path(__file__).parent.parent / "questions.json"


def load_questions() -> list[dict]:
    """Return raw questions list from bundled questions.json."""
    return json.loads(QUESTIONS_FILE.read_text(encoding="utf-8"))


def load_merged_data() -> tuple[list[dict], dict]:
    """
    Returns:
        questions: list of question dicts (read-only data from questions.json)
        progress:  dict of {q_id: {status, note, last_updated}}
    """
    ensure_data_dir()
    questions = load_questions()
    progress = load_progress()
    return questions, progress


def get_topics_ordered(questions: list[dict]) -> list[str]:
    """Return topics in insertion order (preserving questions.json order)."""
    seen: dict[str, None] = {}
    for q in questions:
        seen[q["topic"]] = None
    return list(seen.keys())
