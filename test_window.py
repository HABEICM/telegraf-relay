"""
Simple test to check if PyQt6 window opens
"""
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget
from PyQt6.QtCore import Qt

class TestWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Telegraf Test Window")
        self.setGeometry(100, 100, 600, 400)

        # Central widget
        central = QWidget()
        self.setCentralWidget(central)

        layout = QVBoxLayout(central)

        # Label
        label = QLabel("✅ Telegraf Window Test")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setStyleSheet("""
            QLabel {
                font-size: 32px;
                font-weight: bold;
                color: #4CAF50;
                padding: 20px;
            }
        """)
        layout.addWidget(label)

        # Info
        info = QLabel("If you see this window, PyQt6 is working correctly!")
        info.setAlignment(Qt.AlignmentFlag.AlignCenter)
        info.setStyleSheet("font-size: 16px; padding: 10px;")
        layout.addWidget(info)

        # Button
        btn = QPushButton("Close Test")
        btn.setStyleSheet("""
            QPushButton {
                background: #4CAF50;
                color: white;
                font-size: 16px;
                padding: 15px 30px;
                border-radius: 8px;
                border: none;
            }
            QPushButton:hover {
                background: #45a049;
            }
        """)
        btn.clicked.connect(self.close)
        layout.addWidget(btn)

        # Set background
        self.setStyleSheet("""
            QMainWindow {
                background: white;
            }
        """)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = TestWindow()
    window.show()
    window.raise_()
    window.activateWindow()
    sys.exit(app.exec())
