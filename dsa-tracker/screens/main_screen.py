"""Main screen — virtual-render question browser + stats sidebar."""
from __future__ import annotations

from datetime import date
from textual import on
from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal, Vertical, ScrollableContainer
from textual.message import Message
from textual.screen import Screen
from textual.widget import Widget
from textual.widgets import Input, Static, Button
from rich.text import Text

from data.store import save_progress, update_streak_for_today
from data.loader import get_topics_ordered
from widgets.stats_sidebar import StatsSidebar


DIFF_COLORS  = {"Easy": "#3fb950", "Medium": "#d29922", "Hard": "#f85149"}
PLAT_BADGES  = {
    "LeetCode":      (" LC ", "#58a6ff"),
    "GeeksforGeeks": (" GFG", "#3fb950"),
    "InterviewBit":  (" IB ", "#9b59b6"),
    "CodingNinjas":  (" CN ", "#ff6b35"),
}


# ── Virtual list widget ─────────────────────────────────────────────
class QuestionBrowser(Widget, can_focus=True):
    """Single scrollable widget that renders all questions as Rich text."""

    DEFAULT_CSS = """
    QuestionBrowser {
        height: 1fr;
        background: #0d1117;
        overflow-y: scroll;
        scrollbar-size-vertical: 1;
    }
    QuestionBrowser:focus { border: none; }
    """

    class StatusToggled(Message):
        def __init__(self, q_id: str) -> None:
            super().__init__()
            self.q_id = q_id

    class DetailRequested(Message):
        def __init__(self, question: dict) -> None:
            super().__init__()
            self.question = question

    def __init__(self, questions: list[dict], progress: dict,
                 revision_only: bool = False, **kwargs) -> None:
        super().__init__(**kwargs)
        self.all_questions  = questions
        self.progress       = progress
        self._revision_only = revision_only
        self._filter_diff   = "All"
        self._filter_search = ""
        self._cursor        = 0
        self._expanded: dict[str, bool] = {
            q["topic"]: False for q in questions
        }
        self._before_search_expanded = self._expanded.copy()
        self.search_mode = False
        self._topics_order  = get_topics_ordered(questions)
        self._items: list[tuple] = []
        self._build_items()

    # ── Item list ─────────────────────────────────────────────────
    def _build_items(self) -> None:
        topic_qs: dict[str, list[dict]] = {}
        for q in self.all_questions:
            if self._revision_only and \
               not self.progress.get(q["id"], {}).get("revision"):
                continue
            if self._filter_diff != "All" and q["difficulty"] != self._filter_diff:
                continue
            if self._filter_search and \
               self._filter_search not in q["title"].lower():
                continue
            topic_qs.setdefault(q["topic"], []).append(q)

        if self._filter_search != "" and not self.search_mode:
            # first time entering into search mode
            self.search_mode = True
            self._before_search_expanded = self._expanded.copy()
            self._expanded = {q["topic"]: True for q in self.all_questions}
        elif not self._filter_search != "" and self.search_mode:
            # first time exiting from search mode
            self._expanded = self._before_search_expanded.copy()
            self.search_mode = False
        
        self._items = []
        for t in self._topics_order:
            qs = topic_qs.get(t)
            if not qs:
                continue
            self._items.append(("topic", t))
            if self._expanded.get(t, True):
                for q in qs:
                    self._items.append(("question", q))

        self._cursor = min(self._cursor, max(0, len(self._items) - 1))

    # ── Rendering ─────────────────────────────────────────────────
    def get_content_height(self, container_size, viewport_size, width: int) -> int:
        return max(len(self._items), 1)

    def render(self):
        if not self._items:
            t = Text()
            t.append("\n  No questions found. Try adjusting filters.", style="#484f58")
            return t

        lines: list[Text] = []
        for i, item in enumerate(self._items):
            hl = (i == self._cursor)
            if item[0] == "topic":
                lines.append(self._topic_line(item[1], hl))
            else:
                lines.append(self._question_line(item[1], hl))

        result = Text()
        for i, line in enumerate(lines):
            result.append_text(line)
            if i < len(lines) - 1:
                result.append("\n")
        return result

    def _topic_line(self, topic: str, hl: bool) -> Text:
        all_qs = [q for q in self.all_questions if q["topic"] == topic]
        done   = sum(1 for q in all_qs
                     if self.progress.get(q["id"], {}).get("status") == "done")
        total  = len(all_qs)
        chevron = "▼" if self._expanded.get(topic, True) else "▶"
        n   = round((done / total) * 10) if total else 0
        bar = "█" * n + "░" * (10 - n)
        pct = f"{done/total*100:.0f}%" if total else "0%"
        bg  = " on #1c2128" if hl else " on #161b22"

        t = Text(no_wrap=True)
        t.append(f" {chevron} ", style=f"#484f58{bg}")
        t.append(f"{topic.upper():<83}", style=f"bold #58a6ff{bg}")
        t.append(f"{done:>2}/{total:<2}  ", style=f"#484f58{bg}")
        t.append(bar, style=f"#3fb950{bg}")
        t.append(f" {pct}", style=f"#8b949e{bg}")
        return t

    def _question_line(self, q: dict, hl: bool) -> Text:
        entry = self.progress.get(q["id"], {})
        status = entry.get("status", "todo")
        is_rev = entry.get("revision", False)
        
        cb, cb_style = {
            "done":     ("[✓]", "#3fb950"),
        }.get(status, ("[ ]", "#484f58"))
        rev         = "🟠" if is_rev else "  "
        diff_color  = DIFF_COLORS.get(q["difficulty"], "#c9d1d9")
        diff_badge  = f"[{q['difficulty'][:3].upper()}]"
        plat_label, plat_color = PLAT_BADGES.get(
            q.get("platform", ""), (q.get("platform", "?")[:3], "#8b949e"))
        title = q["title"]
        if len(title) > 37:
            title = title[:36] + "…"
        bg          = " on #1c2128" if hl else ""
        title_color = "#3fb950" if status == "done" else ("#d29922" if is_rev else "#c9d1d9")

        t = Text(no_wrap=True)
        t.append("  ", style=bg)
        t.append(cb,  style=f"{cb_style}{bg}")
        t.append(f" {rev} ", style=f"{'#d29922' if is_rev else '#161b22'}{bg}")
        t.append(f"{title:<85}", style=f"{title_color}{bg}")
        t.append(" ", style=bg)
        t.append(diff_badge, style=f"{diff_color}{bg}")
        t.append(" ", style=bg)
        t.append(plat_label, style=f"{plat_color}{bg}")
        return t

    # ── Keyboard ──────────────────────────────────────────────────
    def on_key(self, event) -> None:
        key = event.key
        if key in ("j", "down"):
            if self._cursor < len(self._items) - 1:
                self._cursor += 1
                self._scroll_cursor()
                self.refresh()
            event.stop()
        elif key in ("k", "up"):
            if self._cursor > 0:
                self._cursor -= 1
                self._scroll_cursor()
                self.refresh()
            event.stop()
        elif key == "space":
            self._handle_space()
            event.stop()
        elif key == "enter":
            self._handle_enter()
            event.stop()

    def _scroll_cursor(self) -> None:
        self.scroll_to(y=max(0, self._cursor - 5), animate=False)

    def _handle_space(self) -> None:
        if not self._items:
            return
        item = self._items[self._cursor]
        if item[0] == "topic":
            t = item[1]
            self._expanded[t] = not self._expanded[t]
            self._build_items()
            self.refresh()
        else:
            self._toggle_status(item[1])

    def _handle_enter(self) -> None:
        if not self._items:
            return
        item = self._items[self._cursor]
        if item[0] == "topic":
            t = item[1]
            self._expanded[t] = not self._expanded[t]
            self._build_items()
            self.refresh()
        else:
            self.post_message(self.DetailRequested(item[1]))

    def _toggle_status(self, q: dict) -> None:
        qid   = q["id"]
        entry = self.progress.get(qid, {})
        new   = "done" if entry.get("status", "todo") != "done" else "todo"
        entry.update({"status": new, "last_updated": date.today().isoformat()})
        entry.setdefault("note", "")
        entry.setdefault("revision", False)
        self.progress[qid] = entry
        save_progress(self.progress)
        update_streak_for_today(self.progress)
        self.refresh()
        self.post_message(self.StatusToggled(qid))

    # ── Public API for MainScreen ─────────────────────────────────
    def set_diff_filter(self, diff: str) -> None:
        self._filter_diff = diff
        self._build_items()
        self.refresh()

    def set_search_filter(self, search: str) -> None:
        self._filter_search = search.lower()
        self._build_items()
        self.refresh()

    def get_current_question(self) -> dict | None:
        if self._items and 0 <= self._cursor < len(self._items):
            item = self._items[self._cursor]
            if item[0] == "question":
                return item[1]
        return None

    def refresh_current(self) -> None:
        """Re-render after external changes (e.g. from detail modal)."""
        self.refresh()


# ── Main Screen ─────────────────────────────────────────────────────
class MainScreen(Screen):
    """Main split-panel screen."""

    BINDINGS = [
        Binding("slash",          "focus_search",          "Search",          show=False),
        Binding("escape",         "clear_search",          "Clear",           show=False),
        Binding("f2",             "toggle_revision_view",  "Revision",        show=False),
        Binding("r",              "toggle_revision_view",  "Revision",        show=False),
        Binding("0",              "filter_all",            "All",             show=False),
        Binding("1",              "filter_easy",           "Easy",            show=False),
        Binding("2",              "filter_medium",         "Medium",          show=False),
        Binding("3",              "filter_hard",           "Hard",            show=False),
        Binding("question_mark",  "show_help",             "Help",            show=False),
        Binding("o",              "open_link",             "Open in browser", show=False),
    ]

    def __init__(self, questions: list[dict], progress: dict,
                 revision_only: bool = False, **kwargs) -> None:
        super().__init__(**kwargs)
        self.questions     = questions
        self.progress      = progress
        self.revision_only = revision_only

    def compose(self) -> ComposeResult:
        with Horizontal(id="main-container"):
            with Vertical(id="left-panel"):
                with Horizontal(id="search-container"):
                    yield Static("🔍 ", id="search-label")
                    yield Input(placeholder="Search questions…", id="search-input")
                with Horizontal(id="diff-tabs"):
                    yield Button("All",    id="tab-all",    classes="diff-tab-active")
                    yield Button("Easy",   id="tab-easy",   classes="diff-tab")
                    yield Button("Medium", id="tab-medium", classes="diff-tab")
                    yield Button("Hard",   id="tab-hard",   classes="diff-tab")
                yield QuestionBrowser(
                    self.questions, self.progress,
                    revision_only=self.revision_only,
                    id="question-browser",
                )
            with Vertical(id="right-panel"):
                yield StatsSidebar(self.questions, self.progress, id="stats-sidebar")

    def on_mount(self) -> None:
        self.query_one("#question-browser", QuestionBrowser).focus()

    # ── Search ────────────────────────────────────────────────────
    @on(Input.Changed, "#search-input")
    def on_search_changed(self, event: Input.Changed) -> None:
        self.query_one("#question-browser", QuestionBrowser).set_search_filter(event.value)

    # ── Diff tabs ─────────────────────────────────────────────────
    @on(Button.Pressed, "#tab-all")
    def tab_all(self)    -> None: self._set_diff("All")
    @on(Button.Pressed, "#tab-easy")
    def tab_easy(self)   -> None: self._set_diff("Easy")
    @on(Button.Pressed, "#tab-medium")
    def tab_medium(self) -> None: self._set_diff("Medium")
    @on(Button.Pressed, "#tab-hard")
    def tab_hard(self)   -> None: self._set_diff("Hard")

    def _set_diff(self, diff: str) -> None:
        for tid, d in [("tab-all","All"),("tab-easy","Easy"),
                       ("tab-medium","Medium"),("tab-hard","Hard")]:
            try:
                self.query_one(f"#{tid}", Button).set_classes(
                    "diff-tab-active" if diff == d else "diff-tab")
            except Exception:
                pass
        self.query_one("#question-browser", QuestionBrowser).set_diff_filter(diff)
        self.query_one("#question-browser", QuestionBrowser).focus()

    # ── Messages from QuestionBrowser ─────────────────────────────
    def on_question_browser_status_toggled(
            self, msg: QuestionBrowser.StatusToggled) -> None:
        self._refresh_stats()

    def on_question_browser_detail_requested(
            self, msg: QuestionBrowser.DetailRequested) -> None:
        self._open_detail(msg.question)

    # ── Actions ───────────────────────────────────────────────────
    def action_focus_search(self)  -> None:
        self.query_one("#search-input", Input).focus()

    def action_clear_search(self) -> None:
        inp = self.query_one("#search-input", Input)
        if inp.value:
            inp.value = ""
            self.query_one("#question-browser", QuestionBrowser).set_search_filter("")
        else:
            inp.blur()
            self.query_one("#question-browser", QuestionBrowser).focus()

    def action_filter_all(self)    -> None: self._set_diff("All")
    def action_filter_easy(self)   -> None: self._set_diff("Easy")
    def action_filter_medium(self) -> None: self._set_diff("Medium")
    def action_filter_hard(self)   -> None: self._set_diff("Hard")

    def action_toggle_revision_view(self) -> None:
        self.app.push_screen(
            MainScreen(self.questions, self.progress,
                       revision_only=not self.revision_only))

    def action_show_help(self) -> None:
        from screens.help_overlay import HelpOverlay
        self.app.push_screen(HelpOverlay())


    # ── Helpers ───────────────────────────────────────────────────
    def _refresh_stats(self) -> None:
        try:
            self.query_one("#stats-sidebar", StatsSidebar).refresh_stats()
        except Exception:
            pass

    def _open_detail(self, q: dict) -> None:
        from screens.detail_modal import DetailModal

        def on_close(saved: bool) -> None:
            if saved:
                browser = self.query_one("#question-browser", QuestionBrowser)
                browser.refresh_current()
                self._refresh_stats()
                if self.revision_only:
                    browser._build_items()
                    browser.refresh()

        self.app.push_screen(DetailModal(q, self.progress), on_close)
