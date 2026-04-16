from textual.app import App, ComposeResult
from textual.containers import Vertical
from screens.main_screen import QuestionBrowser

class TestApp(App):
    def compose(self) -> ComposeResult:
        with Vertical(id="left-panel", styles="height: 1fr; border: solid red;"):
            yield QuestionBrowser(
                questions=[{
                    "id": f"q_{i}", "topic": "Array", "title": f"Q {i}",
                    "difficulty": "Easy", "platform": "LeetCode"
                } for i in range(100)],
                progress={}
            )
            
    def on_mount(self):
        self.query_one(QuestionBrowser).focus()

if __name__ == "__main__":
    app = TestApp()
    app.run(headless=True, size=(80, 20))
