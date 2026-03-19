# Towers of Hanoi Demo

Interactive Towers of Hanoi implementations in two flavors:
- Web app: [`docs/index.html`](docs/index.html) (browser-based Canvas animation)
- Desktop app: [`ToH.py`](ToH.py) (PyQt5)

## Features

- Adjustable disk count (1-15)
- Animated optimal solution
- Reset control
- Live move counter
- Multi-speed animation (web)

## How The Algorithm Works

Both versions use the classic recursive Towers of Hanoi strategy.

To move `n` disks from one tower to another:
1. Move the top `n-1` disks to the helper tower.
2. Move the largest disk (disk `n`) to the target tower.
3. Move the `n-1` disks from the helper tower onto the largest disk.

Pseudo-code:

```text
hanoi(n, source, target, auxiliary):
    if n == 1:
        move source -> target
        return

    hanoi(n-1, source, auxiliary, target)
    move source -> target
    hanoi(n-1, auxiliary, target, source)
```

Minimum number of moves for `n` disks: `2^n - 1`.

## Play Live

Play the live web demo here:

[https://drduke.uk/ToHDemo](https://drduke.uk/ToHDemo)

## Versions

This project includes both a web version and a Python desktop version.

### Web version (`docs/index.html`)
- Runs in a modern browser
- No installation required
- Ideal for quick demos and sharing

### Python version (`ToH.py`)
- Built with PyQt5
- Native desktop UI and animation
- Useful for local/offline use and Python-based teaching sessions

## Quick Start

### Web version
Open [`docs/index.html`](docs/index.html) locally, or use the live site: [https://drduke.uk/ToHDemo](https://drduke.uk/ToHDemo).

### Python version
Install dependencies and run using either `python` or `python3`.

Using `python`:

```bash
python -m pip install --upgrade pip
python -m pip install PyQt5
python ToH.py
```

Using `python3`:

```bash
python3 -m pip install --upgrade pip
python3 -m pip install PyQt5
python3 ToH.py
```

## Notes

- If `PyQt5` is missing, install it in the same Python environment used to run `ToH.py`.
- For the web app, use a modern browser with Canvas support.

## Educational Licence

This project is licensed for educational use.

Full license text is available in [`LICENSE`](LICENSE).

You may use, copy, and adapt this project for:
- Classroom teaching
- Student coursework
- Academic demonstrations and outreach

Not permitted without prior written permission from the author:
- Commercial use
- Resale or paid redistribution

Attribution to the original author must be retained in derivative educational materials.

## Copyright

Copyright Duke Gledhill 2025
