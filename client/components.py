"""
Telegraf UI Components - Glassmorphism Style
Reusable premium UI components
"""

from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

class GlassWidget(QWidget):
    """Base glass effect widget"""
    def __init__(self, parent=None, blur_radius=20, opacity=0.7):
        super().__init__(parent)
        self.blur_radius = blur_radius
        self.opacity = opacity
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Glass background
        path = QPainterPath()
        path.addRoundedRect(QRectF(self.rect()), 15, 15)

        # Background with opacity
        painter.fillPath(path, QColor(255, 255, 255, int(255 * self.opacity * 0.1)))

        # Border
        pen = QPen(QColor(255, 255, 255, 50))
        pen.setWidth(1)
        painter.setPen(pen)
        painter.drawPath(path)


class GlassButton(QPushButton):
    """Glass effect button with hover animation"""
    def __init__(self, text="", icon=None, parent=None):
        super().__init__(text, parent)
        self.setMinimumHeight(40)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        # Animation
        self.hover_animation = QPropertyAnimation(self, b"geometry")
        self.hover_animation.setDuration(200)
        self.hover_animation.setEasingCurve(QEasingCurve.Type.OutCubic)

        self.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(100, 150, 255, 180),
                    stop:1 rgba(150, 100, 255, 180));
                border: 1px solid rgba(255, 255, 255, 100);
                border-radius: 20px;
                color: white;
                font-size: 14px;
                font-weight: 600;
                padding: 10px 20px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(120, 170, 255, 220),
                    stop:1 rgba(170, 120, 255, 220));
                border: 1px solid rgba(255, 255, 255, 150);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(80, 130, 235, 200),
                    stop:1 rgba(130, 80, 235, 200));
            }
        """)


class GlassInput(QLineEdit):
    """Glass effect input field"""
    def __init__(self, placeholder="", parent=None):
        super().__init__(parent)
        self.setPlaceholderText(placeholder)
        self.setMinimumHeight(45)

        self.setStyleSheet("""
            QLineEdit {
                background: rgba(255, 255, 255, 30);
                border: 1px solid rgba(255, 255, 255, 80);
                border-radius: 22px;
                padding: 12px 20px;
                color: white;
                font-size: 14px;
                selection-background-color: rgba(100, 150, 255, 100);
            }
            QLineEdit:focus {
                background: rgba(255, 255, 255, 50);
                border: 2px solid rgba(100, 150, 255, 200);
            }
            QLineEdit::placeholder {
                color: rgba(255, 255, 255, 120);
            }
        """)


class GlassPanel(QFrame):
    """Glass panel with blur effect"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("""
            QFrame {
                background: rgba(20, 30, 50, 180);
                border: 1px solid rgba(255, 255, 255, 50);
                border-radius: 15px;
            }
        """)

        # Add blur effect
        blur = QGraphicsBlurEffect()
        blur.setBlurRadius(10)
        self.setGraphicsEffect(blur)


class MessageBubble(QWidget):
    """Animated message bubble"""
    def __init__(self, text, is_own=False, parent=None):
        super().__init__(parent)
        self.text = text
        self.is_own = is_own
        self.init_ui()

        # Fade in animation
        self.opacity_effect = QGraphicsOpacityEffect()
        self.setGraphicsEffect(self.opacity_effect)

        self.fade_in = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.fade_in.setDuration(300)
        self.fade_in.setStartValue(0)
        self.fade_in.setEndValue(1)
        self.fade_in.setEasingCurve(QEasingCurve.Type.OutCubic)
        self.fade_in.start()

    def init_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 5, 10, 5)

        if not self.is_own:
            layout.addStretch()

        # Message content
        bubble = QLabel(self.text)
        bubble.setWordWrap(True)
        bubble.setMaximumWidth(400)
        bubble.setStyleSheet(f"""
            QLabel {{
                background: {'qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 rgba(100, 150, 255, 200), stop:1 rgba(150, 100, 255, 200))' if self.is_own else 'rgba(40, 50, 70, 200)'};
                border: 1px solid rgba(255, 255, 255, 80);
                border-radius: 18px;
                padding: 12px 16px;
                color: white;
                font-size: 14px;
            }}
        """)
        layout.addWidget(bubble)

        if self.is_own:
            layout.addStretch()


class UserListItem(QWidget):
    """Glass effect user list item"""
    clicked = pyqtSignal(str)

    def __init__(self, user_id, username, status="online", parent=None):
        super().__init__(parent)
        self.user_id = user_id
        self.username = username
        self.status = status
        self.init_ui()

        # Hover effect
        self.setMouseTracking(True)
        self.hovered = False

    def init_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(15, 10, 15, 10)

        # Avatar with status indicator
        avatar_container = QWidget()
        avatar_container.setFixedSize(45, 45)
        avatar_layout = QVBoxLayout(avatar_container)
        avatar_layout.setContentsMargins(0, 0, 0, 0)

        avatar = QLabel()
        avatar.setFixedSize(45, 45)
        avatar.setStyleSheet("""
            QLabel {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(100, 150, 255, 255),
                    stop:1 rgba(150, 100, 255, 255));
                border: 2px solid rgba(255, 255, 255, 100);
                border-radius: 22px;
            }
        """)
        avatar_layout.addWidget(avatar)

        # Status indicator (green dot)
        self.status_indicator = QLabel()
        self.status_indicator.setFixedSize(12, 12)
        self.update_status_indicator()
        self.status_indicator.setStyleSheet("""
            QLabel {
                border-radius: 6px;
                border: 2px solid white;
            }
        """)
        self.status_indicator.move(33, 33)
        self.status_indicator.setParent(avatar_container)

        layout.addWidget(avatar_container)

        # User info
        info_layout = QVBoxLayout()
        info_layout.setSpacing(2)

        self.name_label = QLabel(self.username)
        self.name_label.setStyleSheet("color: white; font-size: 15px; font-weight: 600;")
        info_layout.addWidget(self.name_label)

        self.status_label = QLabel(self.get_status_text())
        self.status_label.setStyleSheet("color: rgba(255, 255, 255, 150); font-size: 12px;")
        info_layout.addWidget(self.status_label)

        layout.addLayout(info_layout)
        layout.addStretch()

    def get_status_text(self):
        """Get status text with emoji"""
        if self.status == "online":
            return "В сети"
        else:
            return "Не в сети"

    def update_status_indicator(self):
        """Update status indicator color"""
        if self.status == "online":
            color = "background: rgba(76, 175, 80, 255);"  # Green
        else:
            color = "background: rgba(158, 158, 158, 255);"  # Gray

        self.status_indicator.setStyleSheet(f"""
            QLabel {{
                {color}
                border-radius: 6px;
                border: 2px solid white;
            }}
        """)

    def set_status(self, status):
        """Update user status"""
        self.status = status
        self.status_label.setText(self.get_status_text())
        self.update_status_indicator()

    def enterEvent(self, event):
        self.hovered = True
        self.setStyleSheet("""
            QWidget {
                background: rgba(255, 255, 255, 30);
                border-radius: 10px;
            }
        """)

    def leaveEvent(self, event):
        self.hovered = False
        self.setStyleSheet("")

    def mousePressEvent(self, event):
        self.clicked.emit(self.user_id)


class SearchBar(QWidget):
    """Glass search bar with live results"""
    search_changed = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(15, 10, 15, 10)

        # Search icon
        icon = QLabel("🔍")
        icon.setStyleSheet("font-size: 18px;")
        layout.addWidget(icon)

        # Search input
        self.search_input = GlassInput("Поиск пользователей...")
        self.search_input.textChanged.connect(self.search_changed.emit)
        layout.addWidget(self.search_input)


class TypingIndicator(QWidget):
    """Animated typing indicator"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
        self.start_animation()

    def init_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(15, 5, 15, 5)

        self.dots = []
        for i in range(3):
            dot = QLabel("●")
            dot.setStyleSheet("color: rgba(100, 150, 255, 200); font-size: 12px;")
            layout.addWidget(dot)
            self.dots.append(dot)

        layout.addStretch()

    def start_animation(self):
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.animate)
        self.timer.start(300)
        self.current_dot = 0

    def animate(self):
        for i, dot in enumerate(self.dots):
            if i == self.current_dot:
                dot.setStyleSheet("color: rgba(100, 150, 255, 255); font-size: 14px;")
            else:
                dot.setStyleSheet("color: rgba(100, 150, 255, 100); font-size: 12px;")

        self.current_dot = (self.current_dot + 1) % 3


class ConnectionStatus(QWidget):
    """Connection status indicator"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 5, 10, 5)

        self.status_dot = QLabel("●")
        self.status_dot.setStyleSheet("color: #4CAF50; font-size: 10px;")
        layout.addWidget(self.status_dot)

        self.status_text = QLabel("Подключено")
        self.status_text.setStyleSheet("color: rgba(255, 255, 255, 180); font-size: 11px;")
        layout.addWidget(self.status_text)

        layout.addStretch()

    def set_status(self, connected):
        if connected:
            self.status_dot.setStyleSheet("color: #4CAF50; font-size: 10px;")
            self.status_text.setText("Подключено")
        else:
            self.status_dot.setStyleSheet("color: #F44336; font-size: 10px;")
            self.status_text.setText("Переподключение...")


class SplashScreen(QWidget):
    """Animated splash screen"""
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        # Removed WA_TranslucentBackground for visibility
        # self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setFixedSize(400, 300)
        self.init_ui()

        # Center on screen
        screen = QApplication.primaryScreen().geometry()
        self.move(
            (screen.width() - self.width()) // 2,
            (screen.height() - self.height()) // 2
        )

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Glass panel
        panel = QWidget()
        panel.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(100, 150, 255, 220),
                    stop:1 rgba(150, 100, 255, 220));
                border: 2px solid rgba(255, 255, 255, 100);
                border-radius: 20px;
            }
        """)

        panel_layout = QVBoxLayout(panel)
        panel_layout.setSpacing(20)

        # Logo
        logo = QLabel("🚀")
        logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo.setStyleSheet("font-size: 64px;")
        panel_layout.addWidget(logo)

        # Title
        title = QLabel("Telegraf")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("color: white; font-size: 32px; font-weight: bold;")
        panel_layout.addWidget(title)

        # Subtitle
        subtitle = QLabel("Premium Messenger")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setStyleSheet("color: rgba(255, 255, 255, 200); font-size: 14px;")
        panel_layout.addWidget(subtitle)

        # Progress
        self.progress = QProgressBar()
        self.progress.setRange(0, 0)  # Indeterminate
        self.progress.setTextVisible(False)
        self.progress.setFixedHeight(4)
        self.progress.setStyleSheet("""
            QProgressBar {
                background: rgba(255, 255, 255, 50);
                border: none;
                border-radius: 2px;
            }
            QProgressBar::chunk {
                background: white;
                border-radius: 2px;
            }
        """)
        panel_layout.addWidget(self.progress)

        layout.addWidget(panel)
