## Towers of Hanoi (ToH) Demo

An interactive Towers of Hanoi demonstration in two flavors:
- **Web**: `ToH.html` — runs in any modern browser using HTML5 Canvas and JavaScript.
- **Desktop**: `ToH.py` — a PyQt5 application with smooth animations and a native UI.

### What’s included
- **Disk selector** (1–15 disks)
- **Start** to animate the optimal solution
- **Reset** to restore the initial state
- **Live move counter**
- **Pleasant visuals** suitable for outreach/demonstrations

---

## Quick Start

### Web version (`ToH.html`)
- Double‑click `ToH.html` or open it in your preferred browser.
- Adjust the number of disks, then click **Start**.
- Click **Reset** to start over.

Tip: Use a modern Chromium, Firefox, or Safari browser.

### Desktop version (`ToH.py`)

#### Prerequisites
- Python 3.8+
- PyQt5

Install PyQt5:
```bash
python3 -m pip install --upgrade pip
python3 -m pip install PyQt5
```

Run the app:
```bash
python3 ToH.py
```

---

## Controls and Behavior
- **Number of Disks**: Select 1–15 disks. More disks = more moves (minimum moves are \(2^n - 1\)).
- **Start**: Generates and animates the optimal solution.
- **Reset**: Stops any running animation and restores the initial stacked state.
- **Move Counter**: Updates as each move completes.

---

## How it works
Both implementations compute the optimal move sequence recursively (classic divide‑and‑conquer):
- Move \(n-1\) disks from source to auxiliary
- Move the largest disk from source to target
- Move \(n-1\) disks from auxiliary to target

Animations are performed in three phases per move (lift → translate → lower) to keep motion smooth and readable.

---

## Customization
- **Disk range**: Adjust the input bounds in `ToH.html` (`min`/`max` on `#diskCount`) or in `ToH.py` (`StyledSpinBox.setRange`).
- **Animation speed**:
  - Web: tweak `animationSpeed` (milliseconds per frame) in `ToH.html`.
  - Desktop: tweak `animation_speed` (milliseconds per frame) in `ToH.py`.
- **Colors**: Both apps generate varied colors per disk; edit the color lists or generation logic if needed.

---

## Troubleshooting
- "ModuleNotFoundError: No module named 'PyQt5'": Install PyQt5 with `python3 -m pip install PyQt5` and ensure you are using the same Python interpreter to run the app.
- macOS Gatekeeper warnings: If launching from Finder fails, run the Python version from Terminal as shown above.
- Browser shows a blank page: Ensure JavaScript is enabled and use a modern browser.

---

## Credits
- UI and implementation © 2025 Duke Gledhill, University of Huddersfield.
- Educational puzzle: Towers of Hanoi (Édouard Lucas, 1883).

---

## License
This demo is provided for educational and outreach use. If you intend to reuse or redistribute, please confirm permissions with the author or your institution’s policy.
