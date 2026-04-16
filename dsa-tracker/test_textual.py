import asyncio
from textual.app import App, ComposeResult
from textual.containers import Vertical
from textual.widget import Widget
from rich.text import Text

class TestWidget(Widget, can_focus=True):
    DEFAULT_CSS = "TestWidget { height: 1fr; overflow-y: auto; }"
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cursor = 0
    def get_content_height(self, a, b, c):
        return 100
    def render(self):
        t = Text()
        for i in range(100):
            t.append(f"Line {i} {'<--' if i == self.cursor else ''}\n")
        return t
    def on_key(self, event):
        if event.key == "down":
            self.cursor = min(99, self.cursor + 1)
            vp_height = max(1, self.size.height)
            if self.cursor >= self.scroll_y + vp_height:
                self.scroll_to(y=self.cursor - vp_height + 1, animate=False)
            self.refresh()
            event.stop()
            with open("scroll_log.txt", "a") as f:
                f.write(f"cursor={self.cursor} vp={vp_height} scroll_y={self.scroll_y} vs={self.virtual_size}\n")

class TestApp(App):
    def compose(self) -> ComposeResult:
        with Vertical(styles="height: 10; border: solid blue;"):
            yield TestWidget()

async def run():
    app = TestApp()
    async with app.run_test() as pilot:
        await pilot.press(*["down"] * 15)
        await asyncio.sleep(0.1)

if __name__ == "__main__":
    asyncio.run(run())
