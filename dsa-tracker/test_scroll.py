from textual.app import App, ComposeResult
from textual.widget import Widget
from rich.text import Text

class CustomScroll(Widget, can_focus=True):
    DEFAULT_CSS = """
    CustomScroll {
        height: 1fr;
        border: solid red;
        overflow-y: scroll;
        scrollbar-size-vertical: 1;
    }
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cursor = 0
    def get_content_height(self, c, v, w):
        return 100
    def render(self):
        t = Text()
        for i in range(100):
            if i == self.cursor:
                t.append(f"Line {i} <---- \n", style="reverse")
            else:
                t.append(f"Line {i}\n")
        return t
    def on_key(self, event):
        if event.key == "down":
            self.cursor = min(99, self.cursor + 1)
            # scroll down if needed
            if self.cursor >= self.scroll_y + self.size.height:
                self.scroll_to(y=self.cursor - self.size.height + 1, animate=False)
            self.refresh()

class MyApp(App):
    def compose(self) -> ComposeResult:
        yield CustomScroll()

if __name__ == "__main__":
    app = MyApp()
    app.run(headless=True, size=(40, 10))
    print("DONE testing")
