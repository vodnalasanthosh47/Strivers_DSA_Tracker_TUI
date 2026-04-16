"""Help overlay — keybinding cheatsheet."""
from __future__ import annotations

from textual.app import ComposeResult
from textual.binding import Binding
from textual.screen import ModalScreen
from textual.widgets import Static
from textual.containers import Vertical


KEYBINDS = [
    ("j / ↓", "Move cursor down"),
    ("k / ↑", "Move cursor up"),
    ("Space", "Toggle done/todo"),
    ("Enter", "Open question detail"),
    ("/", "Focus search bar"),
    ("Esc", "Clear search / close modal"),
    ("F2 / r", "Toggle revision view"),
    ("1 / 2 / 3", "Filter Easy / Medium / Hard"),
    ("0", "Show all difficulties"),
    ("o", "Open link in browser (detail)"),
    ("s", "Save & close (detail)"),
    ("t / d / r", "Set status in detail modal"),
    ("?", "Show this help"),
    ("q", "Quit"),
]


class HelpOverlay(ModalScreen):
    """Keybinding help overlay."""

    BINDINGS = [
        Binding("escape", "close", "Close"),
        Binding("question_mark", "close", "Close"),
        Binding("?", "close", "Close"),
    ]

    def compose(self) -> ComposeResult:
        with Vertical(id="help-container"):
            yield Static(
                "[bold #58a6ff]⌨  KEYBINDINGS — DSA TRACKER[/]",
                id="help-title",
            )
            for key, desc in KEYBINDS:
                yield Static(
                    f"[bold #d29922]{key:<16}[/][#c9d1d9]{desc}[/]",
                    classes="help-row",
                )
            yield Static(
                "[#484f58]Press Esc or ? to close[/]",
                id="help-close-hint",
            )

    def action_close(self) -> None:
        self.dismiss()
