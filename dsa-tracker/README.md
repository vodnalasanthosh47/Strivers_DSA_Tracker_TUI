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
- **Collapsible topic accordion** with per-topic progress bars
- **Live search** — filter by title in real-time
- **Difficulty filter tabs** — All / Easy / Medium / Hard
- **Status tracking** — Todo / Done / Revision per question
- **Notes** — free-text per question, stored locally
- **Revision queue** — `r` or `F2` to see only flagged questions
- **Streak tracker** — daily target (5/day), current streak, all-time best
- **Stats sidebar** — overall %, difficulty breakdown, count badges
- **ASCII art splash** on startup
- **Atomic writes** — no data loss even on crash (`.tmp` → `os.replace`)
- **Zero cloud, zero DB** — all data in `~/.dsa_tracker/` as JSON

---

## 🚀 Quickstart

```bash
# 1. Clone / enter project directory
cd dsa-tracker

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

| Key          | Action                              |
|--------------|-------------------------------------|
| `j` / `↓`   | Move cursor down                    |
| `k` / `↑`   | Move cursor up                      |
| `Space`      | Toggle done / todo on focused item  |
| `Enter`      | Open question detail modal          |
| `/`          | Focus search bar                    |
| `Esc`        | Clear search / close modal          |
| `F2` / `r`  | Toggle revision queue view          |
| `0`          | Show all difficulties               |
| `1`          | Filter: Easy only                   |
| `2`          | Filter: Medium only                 |
| `3`          | Filter: Hard only                   |
| `?`          | Show keybindings help overlay       |
| `q`          | Quit                                |

### Question Detail Modal

| Key    | Action                    |
|--------|---------------------------|
| `t`    | Set status → Todo         |
| `d`    | Set status → Done         |
| `r`    | Set status → Revision     |
| `o`    | Open link in browser      |
| `s`    | Save & close              |
| `Esc`  | Discard & close           |

---

## 📁 File Structure

```
dsa-tracker/
├── main.py                 # Entry point
├── app.py                  # Textual App class + screen routing
├── app.tcss                # Textual CSS theme (dark nerdy aesthetic)
├── questions.json          # 426 questions, read-only
├── requirements.txt
├── screens/
│   ├── splash_screen.py    # ASCII art splash (1.5s)
│   ├── main_screen.py      # Main split-panel screen
│   ├── detail_modal.py     # Question detail overlay
│   └── help_overlay.py     # Keybindings help overlay
├── widgets/
│   └── stats_sidebar.py    # Right-panel stats widget
├── data/
│   ├── loader.py           # Load questions + merge progress
│   └── store.py            # Atomic read/write for JSON files
└── utils/
    └── streaks.py          # Daily streak computation
```

---

## 💾 Data Storage

All data stored in `~/.dsa_tracker/`:

| File            | Contents                                |
|-----------------|-----------------------------------------|
| `progress.json` | Per-question status, notes, timestamps |
| `streaks.json`  | Daily solved counts `{"2026-04-16": 3}` |

Progress is flushed on every status change (Space, modal save). Writes are atomic — data is never corrupted on crash.

### progress.json schema

```json
{
  "q_0": {
    "status": "done",
    "note": "Used modular arithmetic",
    "last_updated": "2026-04-16"
  }
}
```

Status values: `"todo"` | `"done"` | `"revision"`

---

## 🎨 Visual Design

- **Background**: `#0d1117` (GitHub dark)
- **Accent**: `#58a6ff` (blue), `#3fb950` (green), `#d29922` (amber)
- **Done items**: green checkbox `[✓]`
- **Revision items**: amber bookmark `[🔖]`
- **Difficulty badges**: `[EAS]` green | `[MED]` amber | `[HAR]` red
- **Platform badges**: `[LC]` blue | `[GFG]` green | `[IB]` purple | `[CN]` orange
- **Progress bars**: `████████░░░░` style (box-drawing characters)

---

## 🔧 Requirements

- Python 3.10+
- `textual >= 0.50.0`
- `rich >= 13.0.0`
- Terminal with 24-bit color (any modern terminal: kitty, alacritty, iTerm2, Windows Terminal)

---

*Built for nerds who live in the terminal. Happy grinding! 🚀*
