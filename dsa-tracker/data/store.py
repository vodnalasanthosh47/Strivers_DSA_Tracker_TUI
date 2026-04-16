"""Atomic read/write for progress.json stored at ~/.dsa_tracker/progress.json."""
from __future__ import annotations

import json
import os
from datetime import date
from pathlib import Path

DATA_DIR = Path(__file__).parent / "data_files"
PROGRESS_FILE = DATA_DIR / "progress.json"
STREAKS_FILE = DATA_DIR / "streaks.json"


def ensure_data_dir() -> None:
    """Create ~/data_files/ and empty progress.json on first run."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    if not PROGRESS_FILE.exists():
        _write_json(PROGRESS_FILE, {})
    if not STREAKS_FILE.exists():
        _write_json(STREAKS_FILE, {})


def _write_json(path: Path, data: dict) -> None:
    """Atomically write JSON to path using a temp file + os.replace."""
    tmp_path = path.with_suffix(".tmp")
    tmp_path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    os.replace(tmp_path, path)


def load_progress() -> dict:
    """Load and return the progress dict. Returns {} if file missing or corrupt."""
    try:
        content = PROGRESS_FILE.read_text(encoding="utf-8")
        return json.loads(content)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def save_progress(progress: dict) -> None:
    """Atomically write the full progress dict."""
    ensure_data_dir()
    _write_json(PROGRESS_FILE, progress)


def load_streaks() -> dict:
    """Load streaks dict {date_str: count}."""
    try:
        content = STREAKS_FILE.read_text(encoding="utf-8")
        return json.loads(content)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def save_streaks(streaks: dict) -> None:
    """Atomically write streaks dict."""
    ensure_data_dir()
    _write_json(STREAKS_FILE, streaks)


def update_streak_for_today(progress: dict) -> None:
    """Recompute today's count from progress and persist streaks.json."""
    today_str = date.today().isoformat()
    count = sum(
        1
        for v in progress.values()
        if v.get("status") == "done" and v.get("last_updated") == today_str
    )
    streaks = load_streaks()
    streaks[today_str] = count
    save_streaks(streaks)
