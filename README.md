# Towers of Hanoi Demo

Interactive Towers of Hanoi implementations in two flavors:
- Web app: `docs/index.html` (browser-based Canvas animation)
- Desktop app: `ToH.py` (PyQt5)

## Quick Start

### Web version
Open `docs/index.html` in any modern browser.

### Desktop version
Install dependencies and run:

```bash
python -m pip install --upgrade pip
python -m pip install PyQt5
python ToH.py
```

## Features

- Adjustable disk count (1-15)
- Animated optimal solution
- Reset control
- Live move counter
- Multi-speed animation (web)

## Algorithm

Both versions use the classic recursive strategy:

```text
hanoi(n, source, target, auxiliary):
    hanoi(n-1, source, auxiliary, target)
    move disk n from source to target
    hanoi(n-1, auxiliary, target, source)
```

Minimum moves for `n` disks: `2^n - 1`.

## Notes

- If `PyQt5` is missing, install it in the same Python environment used to run `ToH.py`.
- For the web app, use a modern browser with Canvas support.

## Copyright

Copyright Duke Gledhill 2025
