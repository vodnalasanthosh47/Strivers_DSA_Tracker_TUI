# 🧠 DSA Tracker — Striver's A2Z Sheet TUI

A fully-featured, keyboard-first terminal TUI for tracking your progress on [Striver's A2Z DSA Sheet](https://takeuforward.org/strivers-a2z-dsa-course/strivers-a2z-dsa-course-sheet-2/). Built with Python + [Textual](https://github.com/Textualize/textual).

```
 ██████╗ ███████╗ █████╗     ████████╗██████╗  █████╗  ██████╗██╗  ██╗███████╗██████╗
 ██╔══██╗██╔════╝██╔══██╗       ██╔══╝██╔══██╗██╔══██╗██╔════╝██║ ██╔╝██╔════╝██╔══██╗
 ██║  ██║███████╗███████║       ██║   ██████╔╝███████║██║     █████╔╝ █████╗  ██████╔╝
 ██║  ██║╚════██║██╔══██║       ██║   ██╔══██╗██╔══██║██║     ██╔═██╗ ██╔══╝  ██╔══██╗
 ██████╔╝███████║██║  ██║       ██║   ██║  ██║██║  ██║╚██████╗██║  ██╗███████╗██║  ██║
 ╚═════╝ ╚══════╝╚═╝  ╚═╝       ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝
```

---

## ✨ Features

- **426 questions** across 19 topics — Maths → Tries, all of Striver's A2Z
- **Collapsible topic accordion** — all collapsed by default, with per-topic progress bars
- **Virtual scrolling list** — handles all 426 questions with a custom viewport renderer and built-in scrollbar
- **Live search** — `/` to search, filters by title in real-time, expands all topics automatically
- **Difficulty filter tabs** — All / Easy / Medium / Hard (keys `0`–`3`)
- **Todo filter** — `4` to show only incomplete questions (stacks with difficulty filter)
- **Independent revision flag** — mark any question for revision regardless of done/todo status
- **Revision queue** — `r` or `F2` to view only revision-flagged questions
- **Notes** — free-text per question in the detail modal, persisted locally
- **Open in browser** — `o` to open the question link directly from the list or detail modal
- **Streak tracker** — daily target (5/day), current streak, all-time best
- **Stats sidebar** — overall %, difficulty breakdown (Easy/Med/Hard), count badges
- **Atomic writes** — no data loss even on crash (`.tmp` → `os.replace`)
- **Local-first** — all data stored alongside the project in `data/data_files/` as JSON

---

## 🚀 Quickstart

```bash
# 1. Enter project directory
cd Strivers_local

# 2. Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run!
python main.py
```

> **No activation needed if you use:** `.venv/bin/python main.py`

---

## ⌨ Keybinding Cheatsheet

### Global (Main Screen)

| Key         | Action                                        |
|-------------|-----------------------------------------------|
| `j` / `↓`  | Move cursor down                              |
| `k` / `↑`  | Move cursor up                                |
| `Space`     | Toggle done / todo on focused question        |
| `Enter`     | Open question detail modal                    |
| `/`         | Focus search bar                              |
| `Esc`       | Clear search / blur input / close modal       |
| `r` / `F2`  | Toggle revision queue view                    |
| `o`         | Open focused question's link in browser       |
| `0`         | Show all difficulties                         |
| `1`         | Filter: Easy only                             |
| `2`         | Filter: Medium only                           |
| `3`         | Filter: Hard only                             |
| `4`         | Toggle: Todo only (hide completed questions)  |
| `?`         | Show keybindings help overlay                 |
| `q`         | Quit                                          |

### Question Detail Modal

| Key   | Action                                  |
|-------|-----------------------------------------|
| `t`   | Set status → Todo                       |
| `d`   | Set status → Done                       |
| `r`   | Toggle revision flag (independent)      |
| `o`   | Open link in browser                    |
| `s`   | Save & close                            |
| `Esc` | Discard & close                         |

---

## 📁 File Structure

```
Strivers_local/
├── main.py                 # Entry point
├── app.py                  # Textual App class + screen routing
├── app.tcss                # Textual CSS theme (dark nerdy aesthetic)
├── questions.json          # 426 questions, read-only
├── requirements.txt
├── screens/
│   ├── splash_screen.py    # ASCII art splash (1.5s)
│   ├── main_screen.py      # Main split-panel screen + QuestionBrowser
│   ├── detail_modal.py     # Question detail overlay
│   └── help_overlay.py     # Keybindings help overlay
├── widgets/
│   └── stats_sidebar.py    # Right-panel stats widget
├── data/
│   ├── loader.py           # Load questions.json
│   ├── store.py            # Atomic read/write for JSON files
│   └── data_files/
│       ├── progress.json   # Your question progress (auto-created)
│       └── streaks.json    # Daily solve counts (auto-created)
└── utils/
    └── streaks.py          # Daily streak computation
```

---

## 💾 Data Storage

All progress data is stored **locally** in `data/data_files/` (next to the source code):

| File                          | Contents                                    |
|-------------------------------|---------------------------------------------|
| `data/data_files/progress.json` | Per-question status, revision flag, notes, timestamps |
| `data/data_files/streaks.json`  | Daily solved counts `{"2026-04-16": 5}`   |

Progress is flushed on every status change (Space, modal save). Writes are atomic — a `.tmp` file is written and then renamed via `os.replace`, so data is never corrupted on crash.

### progress.json schema

```json
{
  "q_0": {
    "status": "done",
    "revision": false,
    "note": "Used modular arithmetic",
    "last_updated": "2026-04-16"
  },
  "q_37": {
    "status": "done",
    "revision": true,
    "note": "Revisit sliding window variant",
    "last_updated": "2026-02-10"
  }
}
```

- **`status`**: `"todo"` | `"done"`
- **`revision`**: `true` | `false` — independent of status; a done question can still be flagged for revision
- **`note`**: free text
- **`last_updated`**: ISO date string (`YYYY-MM-DD`)

---

## 🎨 Visual Design

- **Background**: `#0d1117` (GitHub dark)
- **Accent**: `#58a6ff` (blue), `#3fb950` (green), `#d29922` (amber)
- **Done items**: green checkbox `[✓]` + green title
- **Revision items**: orange circle `🟠` + amber title (stacks with done)
- **Difficulty badges**: `[EAS]` green | `[MED]` amber | `[HAR]` red
- **Platform badges**: `LC` blue | `GFG` green | `IB` purple | `CN` orange
- **Progress bars**: `████████░░░░` style (block characters)
- **Scrollbar**: custom drawn `█` / ` ` glyph column alongside the question list

---

## 🔧 Requirements

- Python 3.10+
- `textual >= 0.50.0`
- `rich >= 13.0.0`
- Terminal with 24-bit color (kitty, alacritty, iTerm2, Windows Terminal, GNOME Terminal, etc.)

---

*Built for nerds who live in the terminal. Happy grinding! 🚀*
