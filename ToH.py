import tkinter as tk
from tkinter import ttk
import time

class HanoiApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Tower of Hanoi Solver")

        self.canvas = tk.Canvas(root, width=600, height=300, bg="white")
        self.canvas.pack(pady=10)

        control_frame = ttk.Frame(root)
        control_frame.pack()

        ttk.Label(control_frame, text="Number of Disks:").pack(side=tk.LEFT)
        self.disk_var = tk.IntVar(value=3)
        self.disk_spinbox = ttk.Spinbox(control_frame, from_=1, to=8, textvariable=self.disk_var, width=5)
        self.disk_spinbox.pack(side=tk.LEFT, padx=5)

        self.go_button = ttk.Button(control_frame, text="Go", command=self.start)
        self.go_button.pack(side=tk.LEFT, padx=5)

        self.reset_button = ttk.Button(control_frame, text="Reset", command=self.reset)
        self.reset_button.pack(side=tk.LEFT, padx=5)

        self.pegs = [[], [], []]
        self.disks = []
        self.moves = []
        self.running = False

        self.reset()

    def draw(self):
        self.canvas.delete("all")
        peg_width = 10
        peg_height = 200
        peg_spacing = 200
        base_y = 250

        # Draw pegs
        for i in range(3):
            x = 100 + i * peg_spacing
            self.canvas.create_rectangle(x - peg_width//2, base_y - peg_height,
                                         x + peg_width//2, base_y, fill="black")

        # Draw disks
        for peg_index, peg in enumerate(self.pegs):
            for level, disk_id in enumerate(reversed(peg)):
                disk_width = (disk_id + 1) * 20
                x_center = 100 + peg_index * peg_spacing
                y = base_y - (level + 1) * 20
                self.canvas.create_rectangle(x_center - disk_width // 2, y,
                                             x_center + disk_width // 2, y + 20,
                                             fill=f"#8{disk_id+1}{disk_id+1}ff")

        self.root.update()

    def move_disk(self, from_peg, to_peg):
        disk = self.pegs[from_peg].pop()
        self.pegs[to_peg].append(disk)
        self.draw()
        time.sleep(0.5)

    def hanoi(self, n, source, target, auxiliary):
        if n == 1:
            self.moves.append((source, target))
        else:
            self.hanoi(n-1, source, auxiliary, target)
            self.moves.append((source, target))
            self.hanoi(n-1, auxiliary, target, source)

    def run_moves(self):
        self.running = True
        for move in self.moves:
            if not self.running:
                break
            self.move_disk(*move)

    def start(self):
        self.reset()
        n = self.disk_var.get()
        self.hanoi(n, 0, 2, 1)
        self.run_moves()

    def reset(self):
        self.running = False
        n = self.disk_var.get()
        self.pegs = [list(reversed(range(n))), [], []]
        self.moves = []
        self.draw()


if __name__ == "__main__":
    root = tk.Tk()
    app = HanoiApp(root)
    root.mainloop()
