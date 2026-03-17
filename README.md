# Sudoku Game

A classic Sudoku puzzle game built with Python and Pygame, playable both as a desktop app and in the browser via Pygbag. Deployed on Cloudflare Pages.

---

## Live Demo

[Play in Browser](https://sudoku-c90.pages.dev/)

---

## Features

- Three difficulty modes — Easy, Medium, Hard
- Difficulty selector always visible — switch anytime without restarting
- Cell highlighting — selected cell highlights its row, column, and 3×3 box
- Same number highlighting — all matching digits light up on selection
- Hint system — reveals a correct value for a random empty cell
- Solve button — auto-completes the puzzle from its original state
- Unlimited erase — no penalty system, erase and retry freely
- Invalid move detection — incorrect entries shown in red instantly
- Completion message — shows hint count on puzzle completion
- Keyboard support — full keyboard input alongside mouse
- Mobile keyboard support — numeric keyboard triggered on tap in browser

---

## Controls

| Input | Action |
|---|---|
| Click / Tap a cell | Select it |
| `1` – `9` | Enter number in selected cell |
| `Backspace` / `Delete` | Erase selected cell |
| `H` | Hint |
| `S` | Solve |
| `N` | New game |

---

## Project Structure
```
Sudoku-Game/
├── main.py
├── requirements.txt
└── README.md
```

---

## Getting Started Locally

**1. Clone the repository**
```bash
git clone https://github.com/Ayush2029/Sudoku-Game.git
cd Sudoku-Game
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Run the game**
```bash
python sudoku/main.py
```

---

## Dependencies

| Package | Version | Purpose |
|---|---|---|
| pygame | 2.5.2 | Game rendering and input |
| pygbag | 0.9.3 | Build tool for browser/WebAssembly export |

`asyncio`, `random`, `copy`, and `platform` are Python standard library modules — no installation needed.

---

## Building for Browser

Pygbag compiles the Pygame app to WebAssembly so it runs in any browser.
```bash
pip install pygbag
pygbag sudoku/
```

This generates a `sudoku/build/web/` folder. Open `http://localhost:8000` to test locally.

---

## Deploying to Cloudflare Pages

1. Push your repo to GitHub
2. Go to [Cloudflare Pages](https://pages.cloudflare.com) → Create a project → Connect to Git
3. Select your repository
4. Set the following build settings:

| Setting | Value |
|---|---|
| Framework preset | None |
| Build command | `pip install pygbag && pygbag --build main.py` |
| Build output directory | `build/web` |

5. Click **Save and Deploy**

Every push to main will trigger an automatic redeploy.

---

## How It Works

**Puzzle generation** seeds three diagonal 3×3 boxes with random numbers, solves the full board using backtracking, then removes a set number of cells based on difficulty.

| Difficulty | Cells removed |
|---|---|
| Easy | 36 |
| Medium | 46 |
| Hard | 56 |

**Solver** uses recursive backtracking — tries digits 1–9 in each empty cell, backtracks on dead ends until the board is fully solved.

**Browser compatibility** is achieved via `asyncio` — the game loop uses `await asyncio.sleep(0)` each frame to yield control back to the browser, preventing tab freezes.

---

## Tech Stack

- **Python 3.x**
- **Pygame 2.5.2** — rendering, input, fonts
- **Pygbag 0.9.3** — WebAssembly build
- **Cloudflare Pages** — hosting

---

## License

MIT
