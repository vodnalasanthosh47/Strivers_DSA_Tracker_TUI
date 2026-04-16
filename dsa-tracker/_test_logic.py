"""Quick sanity tests — no Textual runtime needed."""
import sys
sys.path.insert(0, '.')

from data.loader import load_merged_data, get_topics_ordered
from data.store import ensure_data_dir
from utils.streaks import compute_streaks, DAILY_TARGET
from widgets.stats_sidebar import _bar

ensure_data_dir()
questions, progress = load_merged_data()
print(f"OK: {len(questions)} questions loaded")

topics = get_topics_ordered(questions)
print(f"OK: {len(topics)} topics — first 4: {topics[:4]}")

bar = _bar(50, 100, 20)
assert len(bar) == 20, f"Expected bar length 20, got {len(bar)}"
print(f"OK: bar=[{bar}]")

today_count, cur, best, target = compute_streaks()
assert target == 5 == DAILY_TARGET
print(f"OK: streaks today={today_count} cur={cur} best={best} target={target}")

# Check platform coverage in questions
platforms = set(q.get('platform','') for q in questions)
print(f"OK: platforms={platforms}")

print("\n✅ All logic checks passed!")
