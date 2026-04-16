"""Stats sidebar widget — shows progress, streaks, difficulty breakdown."""
from __future__ import annotations

from datetime import date
from textual.app import ComposeResult
from textual.reactive import reactive
from textual.widget import Widget
from textual.widgets import Static


def _bar(filled: int, total: int, width: int = 20) -> str:
    """Build a █░ style text progress bar."""
    if total == 0:
        frac = 0.0
    else:
        frac = filled / total
    n = round(frac * width)
    return "█" * n + "░" * (width - n)


def _diff_bar(filled: int, total: int, width: int = 14) -> str:
    if total == 0:
        return "░" * width
    n = round((filled / total) * width)
    return "█" * n + "░" * (width - n)


class StatsSidebar(Widget):
    """Right-panel stats widget. Call refresh_stats() after any progress change."""

    DEFAULT_CSS = ""

    def __init__(
        self,
        questions: list[dict],
        progress: dict,
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)
        self.questions = questions
        self.progress = progress

    def compose(self) -> ComposeResult:
        yield Static("", id="stats-body")

    def on_mount(self) -> None:
        self.refresh_stats()

    def refresh_stats(self) -> None:
        """Recompute all stats and re-render."""
        from utils.streaks import compute_streaks

        total = len(self.questions)
        done_ids = {
            qid for qid, v in self.progress.items() if v.get("status") == "done"
        }
        revision_ids = {
            qid for qid, v in self.progress.items() if v.get("revision") is True
        }
        done_count = len(done_ids)
        todo_count = total - done_count
        rev_count = len(revision_ids)

        pct = (done_count / total * 100) if total else 0

        # Difficulty breakdown
        diff_counts: dict[str, tuple[int, int]] = {}
        for q in self.questions:
            d = q["difficulty"]
            qid = q["id"]
            done_q = qid in done_ids
            diff_counts.setdefault(d, [0, 0])
            diff_counts[d][1] += 1
            if done_q:
                diff_counts[d][0] += 1

        easy_done, easy_total = diff_counts.get("Easy", [0, 0])
        med_done, med_total = diff_counts.get("Medium", [0, 0])
        hard_done, hard_total = diff_counts.get("Hard", [0, 0])

        today_count, cur_streak, best_streak, daily_target = compute_streaks()

        # Build the big text block
        bar20 = _bar(done_count, total, 22)
        daily_bar = _bar(today_count, daily_target, 18)
        easy_bar = _diff_bar(easy_done, easy_total, 12)
        med_bar = _diff_bar(med_done, med_total, 12)
        hard_bar = _diff_bar(hard_done, hard_total, 12)

        today_str = date.today().strftime("%a, %b %d")

        lines = [
            f"[bold #58a6ff]┌─ STRIVER'S A2Z DSA SHEET ─┐[/]",
            f"[#484f58]  Keyboard-first progress\n[#484f58]  tracker [/]",
            "",
            f"[bold #8b949e]── DAILY TARGET ({today_str}) ──[/]",
            f"  [#c9d1d9]{daily_bar}[/] [bold]{today_count}[/][#484f58]/{daily_target}[/]",
            f"  [#484f58]🔥 Streak:[/] [bold #d29922]{cur_streak}[/][#484f58]d  Best:[/] [bold #3fb950]{best_streak}[/][#484f58]d[/]",
            "",
            f"[bold #8b949e]── OVERALL PROGRESS ──[/]",
            f"  [bold #3fb950]{pct:5.1f}%[/] complete",
            f"  [#3fb950]{bar20}[/]",
            f"  [#484f58]Done[/] [bold #3fb950]{done_count:>3}[/]  [#484f58]Left[/] [bold #c9d1d9]{todo_count:>3}[/]  [#484f58]Rev[/] [bold #d29922]{rev_count:>3}[/]",
            "",
            f"[bold #8b949e]── STATUS COUNTS ──[/]",
            f"  [#3fb950]■[/] Done      [bold #3fb950]{done_count:>4}[/] / {total}",
            f"  [#d29922]■[/] Revision  [bold #d29922]{rev_count:>4}[/]",
            f"  [#484f58]■[/] Todo      [bold #484f58]{todo_count:>4}[/]",
            "",
            f"[bold #8b949e]── DIFFICULTY BREAKDOWN ──[/]",
            f"  [bold #3fb950]EASY  [/] [#3fb950]{easy_bar}[/] [bold]{easy_done}[/][#484f58]/{easy_total}[/]",
            f"  [bold #d29922]MED   [/] [#d29922]{med_bar}[/] [bold]{med_done}[/][#484f58]/{med_total}[/]",
            f"  [bold #f85149]HARD  [/] [#f85149]{hard_bar}[/] [bold]{hard_done}[/][#484f58]/{hard_total}[/]",
            "",
            f"[bold #8b949e]── QUICK KEYS ──[/]",
            f"  [#d29922]/[/] search  [#d29922]Space[/] toggle",
            f"  [#d29922]Enter[/] detail  [#d29922]r[/] revision",
            f"  [#d29922]0-3[/] filter  [#d29922]?[/] help  [#d29922]q[/] quit",
        ]

        markup = "\n".join(lines)
        self.query_one("#stats-body", Static).update(markup)
