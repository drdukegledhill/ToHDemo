from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                           QHBoxLayout, QPushButton, QSpinBox, QLabel, QFrame)
from PyQt5.QtGui import QPainter, QColor, QBrush, QFont, QPen, QLinearGradient
from PyQt5.QtCore import Qt, QTimer, QPointF
import sys
import random

class TowerWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(800, 400)
        self.disks = []
        self.towers = [[], [], []]
        self.moves = []
        self.current_move = 0
        self.animation_speed = 10
        self.is_animating = False
        
        # Store disk colors
        self.disk_colors = {}  # Will store disk_size: (color1, color2) pairs
        
        # Animation state
        self.moving_disk = None
        self.moving_disk_pos = QPointF(0, 0)
        self.animation_step = 0
        self.source_x = 0
        self.target_x = 0
        self.source_y = 0
        self.target_y = 0
        
        # Define pole positions as constants
        self.POLE_POSITIONS = [200, 400, 600]
        
        # Set background color
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(self.backgroundRole(), QColor("#F5F5F7"))
        self.setPalette(palette)

    def generate_random_color_pair(self):
        """Generate a pair of colors for gradient effect"""
        # List of pleasant colors (hex values)
        colors = [
            "#FF3B30", "#FF9500", "#FFCC00", "#4CD964", "#5856D6", "#007AFF", 
            "#5AC8FA", "#AF52DE", "#FF2D55", "#E35C3B", "#30B0C7", "#2ED157",
            "#64D2FF", "#FF375F", "#FFD60A", "#BF5AF2"
        ]
        
        # Pick a random color and create a slightly darker variant
        base_color = QColor(random.choice(colors))
        h, s, v, _ = base_color.getHsv()
        darker_color = QColor.fromHsv(h, min(s + 20, 255), max(v - 30, 0))
        
        return base_color, darker_color

    def initialize_disk_colors(self, n):
        """Initialize colors for n disks"""
        self.disk_colors.clear()
        for disk_size in range(1, n + 1):
            self.disk_colors[disk_size] = self.generate_random_color_pair()

    def draw_disk(self, painter, x, y, width, disk_size, is_moving=False):
        """Draw a disk with its assigned colors"""
        # Draw disk shadow
        shadow_color = QColor(0, 0, 0, 30)
        painter.fillRect(x - width//2 + 2, y + 2, width, 15, shadow_color)
        
        # Get or generate colors for this disk
        if disk_size not in self.disk_colors:
            self.disk_colors[disk_size] = self.generate_random_color_pair()
        color1, color2 = self.disk_colors[disk_size]
        
        # Create disk gradient
        disk_gradient = QLinearGradient(x - width//2, y, x + width//2, y)
        if is_moving:
            disk_gradient.setColorAt(0, color2)
            disk_gradient.setColorAt(1, color1)
        else:
            disk_gradient.setColorAt(0, color1)
            disk_gradient.setColorAt(1, color2)
        
        # Draw disk with rounded corners
        painter.setPen(Qt.NoPen)
        painter.setBrush(disk_gradient)
        painter.drawRoundedRect(x - width//2, y, width, 15, 7, 7)

    def get_disk_position(self, tower_idx, height):
        """Calculate the x, y position for a disk"""
        x = self.POLE_POSITIONS[tower_idx]  # Use constant pole positions
        y = 340 - height * 20
        return x, y

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Draw base with gradient
        base_gradient = QLinearGradient(50, 345, 750, 345)
        base_gradient.setColorAt(0, QColor("#2C2C2E"))
        base_gradient.setColorAt(1, QColor("#3A3A3C"))
        painter.fillRect(50, 345, 700, 20, base_gradient)
        
        # Draw poles with gradient
        pole_gradient = QLinearGradient(0, 100, 0, 350)
        pole_gradient.setColorAt(0, QColor("#8B4513"))
        pole_gradient.setColorAt(1, QColor("#654321"))
        
        for x in self.POLE_POSITIONS:
            # Draw pole shadow
            shadow_color = QColor(0, 0, 0, 30)
            painter.fillRect(x-3, 100, 16, 250, shadow_color)
            # Draw pole
            painter.fillRect(x-5, 100, 10, 250, pole_gradient)

        # Draw stationary disks
        for tower_idx, tower in enumerate(self.towers):
            x_base = self.POLE_POSITIONS[tower_idx]
            for disk_idx, disk_size in enumerate(tower):
                if disk_size != self.moving_disk:
                    y = 340 - disk_idx * 20
                    width = disk_size * 20
                    self.draw_disk(painter, x_base, y, width, disk_size)

        # Draw moving disk
        if self.moving_disk is not None:
            width = self.moving_disk * 20
            self.draw_disk(painter, 
                          self.moving_disk_pos.x(), 
                          self.moving_disk_pos.y(), 
                          width, 
                          self.moving_disk, 
                          True)

class StyledSpinBox(QSpinBox):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("""
            QSpinBox {
                background-color: white;
                border: 1px solid #CCCCCC;
                border-radius: 6px;
                padding: 5px;
                min-width: 70px;
                min-height: 25px;
            }
            QSpinBox::up-button, QSpinBox::down-button {
                border: none;
                background: #E5E5EA;
                border-radius: 4px;
                margin: 1px;
            }
            QSpinBox::up-button:hover, QSpinBox::down-button:hover {
                background: #D1D1D6;
            }
        """)

class TowersOfHanoi(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Towers of Hanoi - University of Huddersfield")
        self.setMinimumSize(800, 550)
        self.setStyleSheet("""
            QMainWindow {
                background-color: #F5F5F7;
            }
            QPushButton {
                background-color: #007AFF;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 8px 16px;
                font-size: 14px;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #0066CC;
            }
            QPushButton:disabled {
                background-color: #B4B4B4;
            }
            QLabel {
                color: #1D1D1F;
            }
        """)

        # Create main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)
        layout.setSpacing(20)
        layout.setContentsMargins(20, 20, 20, 20)

        # Add title with modern styling
        title_label = QLabel("University of Huddersfield")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setFont(QFont('SF Pro Display', 24, QFont.Bold))
        title_label.setStyleSheet("color: #1D1D1F; margin-bottom: 10px;")
        layout.addWidget(title_label)

        # Create control panel with modern styling
        control_panel = QFrame()
        control_panel.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 10px;
                padding: 10px;
            }
        """)
        control_layout = QHBoxLayout(control_panel)
        control_layout.setContentsMargins(20, 10, 20, 10)
        
        # Create disk number selector
        self.disk_spinner = StyledSpinBox()
        self.disk_spinner.setRange(1, 15)
        self.disk_spinner.setValue(3)
        self.disk_spinner.valueChanged.connect(self.initialize_towers)
        
        disk_label = QLabel("Number of Disks:")
        disk_label.setFont(QFont('SF Pro Text', 14))
        control_layout.addWidget(disk_label)
        control_layout.addWidget(self.disk_spinner)
        
        control_layout.addStretch()
        
        # Create buttons
        self.start_button = QPushButton("Start")
        self.start_button.clicked.connect(self.start_animation)
        control_layout.addWidget(self.start_button)
        
        self.reset_button = QPushButton("Reset")
        self.reset_button.clicked.connect(self.reset_towers)
        self.reset_button.setStyleSheet("""
            QPushButton {
                background-color: #FF3B30;
            }
            QPushButton:hover {
                background-color: #FF2D55;
            }
        """)
        control_layout.addWidget(self.reset_button)
        
        layout.addWidget(control_panel)

        # Add move counter
        self.move_counter_label = QLabel("Moves: 0")
        self.move_counter_label.setFont(QFont('SF Pro Display', 20, QFont.Bold))
        self.move_counter_label.setAlignment(Qt.AlignCenter)
        self.move_counter_label.setStyleSheet("color: #1D1D1F; margin: 10px 0;")
        layout.addWidget(self.move_counter_label)

        # Create tower widget with shadow effect
        self.tower_widget = TowerWidget()
        self.tower_widget.setStyleSheet("""
            QWidget {
                background-color: white;
                border-radius: 10px;
            }
        """)
        layout.addWidget(self.tower_widget)

        # Add copyright with modern styling
        copyright_label = QLabel("Copyright Duke Gledhill 2025")
        copyright_label.setAlignment(Qt.AlignCenter)
        copyright_label.setFont(QFont('SF Pro Text', 12))
        copyright_label.setStyleSheet("color: #86868B;")
        layout.addWidget(copyright_label)

        # Initialize
        self.initialize_towers()

    def initialize_towers(self):
        n = self.disk_spinner.value()
        self.tower_widget.towers = [list(range(n, 0, -1)), [], []]
        self.tower_widget.moves = []
        self.tower_widget.current_move = 0
        self.tower_widget.is_animating = False
        self.tower_widget.moving_disk = None
        self.tower_widget.moving_disk_pos = QPointF(0, 0)
        self.tower_widget.animation_step = 0
        self.move_counter_label.setText("Moves: 0")
        # Initialize new random colors for all disks
        self.tower_widget.initialize_disk_colors(n)
        self.tower_widget.update()
        print(f"Initialized towers with {n} disks")
        
    def reset_towers(self):
        if self.tower_widget.is_animating:
            self.tower_widget.is_animating = False
            self.tower_widget.moving_disk = None  # Clear any moving disk
            self.tower_widget.moving_disk_pos = QPointF(0, 0)  # Reset position
        self.start_button.setEnabled(True)
        self.initialize_towers()
        print("Reset completed")

    def solve_hanoi(self, n, source, target, auxiliary):
        if n > 0:
            self.solve_hanoi(n-1, source, auxiliary, target)
            self.tower_widget.moves.append((source, target))
            self.solve_hanoi(n-1, auxiliary, target, source)

    def animate_disk_movement(self):
        """Handle the smooth disk animation"""
        if not self.tower_widget.is_animating or self.tower_widget.moving_disk is None:
            return

        TOTAL_STEPS = 10  # Kept small for faster animation
        
        # Calculate the current animation phase
        if self.tower_widget.animation_step < TOTAL_STEPS:  # Moving up
            progress = self.tower_widget.animation_step / TOTAL_STEPS
            self.tower_widget.moving_disk_pos.setY(
                self.tower_widget.source_y - (progress * 240)
            )
        elif self.tower_widget.animation_step < TOTAL_STEPS * 2:  # Moving sideways
            progress = (self.tower_widget.animation_step - TOTAL_STEPS) / TOTAL_STEPS
            self.tower_widget.moving_disk_pos.setX(
                self.tower_widget.source_x + (self.tower_widget.target_x - self.tower_widget.source_x) * progress
            )
        elif self.tower_widget.animation_step < TOTAL_STEPS * 3:  # Moving down
            progress = (self.tower_widget.animation_step - TOTAL_STEPS * 2) / TOTAL_STEPS
            self.tower_widget.moving_disk_pos.setY(
                100 + (self.tower_widget.target_y - 100) * progress
            )
        else:  # Animation complete
            # Complete the move
            self.tower_widget.towers[self.current_target].append(self.tower_widget.moving_disk)
            self.tower_widget.moving_disk = None
            self.tower_widget.current_move += 1
            self.move_counter_label.setText(f"Moves: {self.tower_widget.current_move}")
            
            # Start next move or finish
            if self.tower_widget.current_move >= len(self.tower_widget.moves):
                self.tower_widget.is_animating = False
                self.start_button.setEnabled(True)
                print("Animation completed")
            else:
                self.start_disk_movement()
            
            self.tower_widget.update()
            return

        self.tower_widget.animation_step += 1
        self.tower_widget.update()
        QTimer.singleShot(self.tower_widget.animation_speed, self.animate_disk_movement)

    def start_disk_movement(self):
        """Start the animation for the next disk movement"""
        if self.tower_widget.current_move >= len(self.tower_widget.moves):
            return

        self.current_source, self.current_target = self.tower_widget.moves[self.tower_widget.current_move]
        
        # Get the disk to move
        self.tower_widget.moving_disk = self.tower_widget.towers[self.current_source].pop()
        
        # Calculate start and end positions
        source_height = len(self.tower_widget.towers[self.current_source])
        target_height = len(self.tower_widget.towers[self.current_target])
        
        self.tower_widget.source_x, self.tower_widget.source_y = self.tower_widget.get_disk_position(
            self.current_source, source_height
        )
        self.tower_widget.target_x, self.tower_widget.target_y = self.tower_widget.get_disk_position(
            self.current_target, target_height
        )
        
        # Set initial position
        self.tower_widget.moving_disk_pos = QPointF(
            self.tower_widget.source_x,
            self.tower_widget.source_y
        )
        
        # Reset animation step counter
        self.tower_widget.animation_step = 0
        
        # Start the animation
        self.animate_disk_movement()

    def animate_move(self):
        if not self.tower_widget.is_animating:
            print("Animation stopped")
            return
            
        self.start_disk_movement()

    def start_animation(self):
        if self.tower_widget.is_animating:
            return

        print("Starting animation...")
        
        # Store the current disk colors
        saved_colors = self.tower_widget.disk_colors.copy()
        
        # Reset the state completely before starting new animation
        n = self.disk_spinner.value()
        self.tower_widget.towers = [list(range(n, 0, -1)), [], []]
        self.tower_widget.moves = []
        self.tower_widget.current_move = 0
        self.tower_widget.is_animating = False
        self.tower_widget.moving_disk = None
        self.tower_widget.moving_disk_pos = QPointF(0, 0)
        self.tower_widget.animation_step = 0
        self.move_counter_label.setText("Moves: 0")
        
        # Restore the saved disk colors
        self.tower_widget.disk_colors = saved_colors
        
        self.tower_widget.is_animating = True
        self.start_button.setEnabled(False)
        
        # Generate solution moves
        self.tower_widget.moves = []
        self.solve_hanoi(n, 0, 2, 1)
        print(f"Generated {len(self.tower_widget.moves)} moves")
        
        # Start animation
        QTimer.singleShot(self.tower_widget.animation_speed, self.animate_move)

def main():
    app = QApplication(sys.argv)
    window = TowersOfHanoi()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()