"""Detail modal — question detail overlay with status selector and notes."""
from __future__ import annotations

import webbrowser
from datetime import date

from textual import on
from textual.app import ComposeResult
from textual.binding import Binding
from textual.screen import ModalScreen
from textual.widgets import Button, Static, TextArea
from textual.containers import Vertical, Horizontal

from data.store import save_progress, update_streak_for_today


class DetailModal(ModalScreen):
    """Modal overlay for viewing/editing a single question."""

    BINDINGS = [
        Binding("escape", "discard_close", "Discard & close"),
        Binding("s", "save_close", "Save & close"),
        Binding("o", "open_link", "Open in browser"),
        Binding("t", "set_todo", "Set Todo"),
        Binding("d", "set_done", "Set Done"),
        Binding("r", "set_revision", "Set Revision"),
    ]

    def __init__(self, question: dict, progress: dict, **kwargs) -> None:
        super().__init__(**kwargs)
        self.question = question
        self.progress = progress  # shared mutable dict
        self._current_status = progress.get(question["id"], {}).get("status", "todo")
        self._note = progress.get(question["id"], {}).get("note", "")

    def compose(self) -> ComposeResult:
        q = self.question
        diff = q["difficulty"]
        diff_color = {"Easy": "#3fb950", "Medium": "#d29922", "Hard": "#f85149"}.get(diff, "#c9d1d9")
        platform = q.get("platform", "")
        PLAT_SHORT = {
            "LeetCode": "LC", "GeeksforGeeks": "GFG",
            "InterviewBit": "IB", "CodingNinjas": "CN",
        }
        PLAT_COLOR = {
            "LeetCode": "#58a6ff", "GeeksforGeeks": "#3fb950",
            "InterviewBit": "#9b59b6", "CodingNinjas": "#ff6b35",
        }
        plat_short = PLAT_SHORT.get(platform, platform[:3])
        plat_color = PLAT_COLOR.get(platform, "#8b949e")

        with Vertical(id="modal-container"):
            yield Static(
                f"[bold #c9d1d9]{q['title']}[/]",
                id="modal-title",
            )
            yield Static(
                f"[#484f58]{q['topic']}[/]",
                id="modal-breadcrumb",
            )
            yield Static(
                f" [{diff_color}][{diff.upper()}][/]   [{plat_color}][{plat_short}][/] [#484f58]{platform}[/]",
                id="modal-badges",
            )
            yield Static(
                f"[#484f58]Link:[/] [#58a6ff]{q['link']}[/]",
                id="modal-link",
            )
            yield Static("[#8b949e]Status:[/]", classes="stats-section-title")
            with Horizontal(id="modal-status-row"):
                yield Button("[ Todo ]", id="btn-todo", classes="modal-status-btn")
                yield Button("[✓ Done ]", id="btn-done", classes="modal-status-btn")
                yield Button("[🔖 Revision]", id="btn-revision", classes="modal-status-btn")
            yield Static("[#8b949e]Notes:[/]", id="modal-notes-label")
            yield TextArea(self._note, id="modal-notes")
            yield Static(
                "[#484f58]o[/][#8b949e] open link  [/][#484f58]d/t/r[/][#8b949e] status  [/][#484f58]s[/][#8b949e] save  [/][#484f58]Esc[/][#8b949e] discard[/]",
                id="modal-keybinds",
            )

    def on_mount(self) -> None:
        self._update_status_buttons()

    def _update_status_buttons(self) -> None:
        s = self._current_status
        todo_cls = "modal-status-btn--active-todo" if s == "todo" else "modal-status-btn"
        done_cls = "modal-status-btn--active-done" if s == "done" else "modal-status-btn"
        rev_cls = "modal-status-btn--active-revision" if s == "revision" else "modal-status-btn"
        self.query_one("#btn-todo", Button).set_classes(todo_cls)
        self.query_one("#btn-done", Button).set_classes(done_cls)
        self.query_one("#btn-revision", Button).set_classes(rev_cls)

    @on(Button.Pressed, "#btn-todo")
    def press_todo(self) -> None:
        self._current_status = "todo"
        self._update_status_buttons()

    @on(Button.Pressed, "#btn-done")
    def press_done(self) -> None:
        self._current_status = "done"
        self._update_status_buttons()

    @on(Button.Pressed, "#btn-revision")
    def press_revision(self) -> None:
        self._current_status = "revision"
        self._update_status_buttons()

    def action_set_todo(self) -> None:
        self._current_status = "todo"
        self._update_status_buttons()

    def action_set_done(self) -> None:
        self._current_status = "done"
        self._update_status_buttons()

    def action_set_revision(self) -> None:
        self._current_status = "revision"
        self._update_status_buttons()

    def action_open_link(self) -> None:
        webbrowser.open(self.question["link"])

    def _save(self) -> None:
        qid = self.question["id"]
        note_text = self.query_one("#modal-notes", TextArea).text
        entry = self.progress.get(qid, {})
        entry["status"] = self._current_status
        entry["note"] = note_text
        if self._current_status == "done":
            entry["last_updated"] = date.today().isoformat()
        elif "last_updated" not in entry:
            entry["last_updated"] = date.today().isoformat()
        self.progress[qid] = entry
        save_progress(self.progress)
        update_streak_for_today(self.progress)

    def action_save_close(self) -> None:
        self._save()
        self.dismiss(True)

    def action_discard_close(self) -> None:
        self.dismiss(False)
