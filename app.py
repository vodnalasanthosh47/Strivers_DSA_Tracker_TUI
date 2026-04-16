"""Main Textual App class — screen routing and global keybinds."""
from __future__ import annotations

from textual.app import App, ComposeResult
from textual.binding import Binding

from data.loader import load_merged_data
from data.store import ensure_data_dir
from screens.splash_screen import SplashScreen
from screens.main_screen import MainScreen


class DSATrackerApp(App):
    """Striver's A2Z DSA Sheet Terminal Tracker."""

    CSS_PATH = "app.tcss"
    TITLE = "DSA Tracker"
    SUB_TITLE = "Striver's A2Z Sheet"

    BINDINGS = [
        Binding("q", "quit", "Quit", show=True),
    ]

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        ensure_data_dir()
        self.questions, self.progress = load_merged_data()

    def on_mount(self) -> None:
        # Register screens
        self.install_screen(SplashScreen(), name="splash")
        self.install_screen(
            MainScreen(self.questions, self.progress),
            name="main",
        )
        self.push_screen("splash")

    def action_quit(self) -> None:
        self.exit()
