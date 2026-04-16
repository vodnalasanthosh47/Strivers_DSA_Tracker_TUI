"""Streak computation utilities."""
from __future__ import annotations

from datetime import date, timedelta

from data.store import load_streaks

DAILY_TARGET = 5


def compute_streaks() -> tuple[int, int, int, int]:
    """
    Returns:
        today_count    - questions marked done today
        current_streak - consecutive days ending today or yesterday
        best_streak    - all-time max streak
        today_target   - hardcoded DAILY_TARGET
    """
    streaks_data = load_streaks()
    today = date.today()
    today_str = today.isoformat()

    today_count = streaks_data.get(today_str, 0)

    # Compute current streak
    current_streak = 0
    check_date = today
    # Allow today OR start from yesterday if today hasn't been logged yet
    while True:
        ds = check_date.isoformat()
        if streaks_data.get(ds, 0) >= 1:
            current_streak += 1
            check_date -= timedelta(days=1)
        else:
            break

    # Best streak: window scan over all dates
    if not streaks_data:
        best_streak = 0
    else:
        # Sort all dates
        all_dates = sorted(date.fromisoformat(d) for d in streaks_data if streaks_data[d] >= 1)
        if not all_dates:
            best_streak = 0
        else:
            best = 1
            run = 1
            for i in range(1, len(all_dates)):
                if (all_dates[i] - all_dates[i - 1]).days == 1:
                    run += 1
                    best = max(best, run)
                else:
                    run = 1
            best_streak = best

    return today_count, current_streak, best_streak, DAILY_TARGET
