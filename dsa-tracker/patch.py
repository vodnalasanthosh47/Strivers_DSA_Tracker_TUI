import re

with open("screens/main_screen.py", "r") as f:
    text = f.read()

patch = """    def _scroll_cursor(self) -> None:
        viewport_height = max(1, self.size.height)
        with open("debug_scroll.txt", "a") as f:
            f.write(f"cursor={self._cursor} scroll_y={self.scroll_y} size.height={self.size.height} virtual_size.height={self.virtual_size.height}\\n")
        
        if self._cursor < self.scroll_y:
            self.scroll_to(y=self._cursor, animate=False)
        elif self._cursor >= self.scroll_y + viewport_height:
            self.scroll_to(y=self._cursor - viewport_height + 1, animate=False)
"""

text = re.sub(r'    def _scroll_cursor\(self\) -> None:.*?elif self\._cursor >= self\.scroll_y \+ viewport_height:\n            self\.scroll_to\(y=self\._cursor - viewport_height \+ 1, animate=False\)\n', patch, text, flags=re.DOTALL)

with open("screens/main_screen.py", "w") as f:
    f.write(text)
print("Patched main_screen.py for logging")

