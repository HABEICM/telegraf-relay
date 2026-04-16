"""
Telegraf Client - Modern Edition
Clean, minimalistic messenger inspired by Telegram
"""

import sys
import json
import asyncio
import websockets
import ssl
import traceback
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from datetime import datetime
import hashlib
from pathlib import Path

# Setup logging first
try:
    from logger import logger
except ImportError:
    import logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

logger.info("Starting Telegraf Client...")

try:
    from encryption import EncryptionManager
    from database import UserDatabase
    from components import (
        ModernButton, ModernInput, SearchBar, MessageBubble,
        UserListItem, TypingIndicator, ConnectionStatus,
        SplashScreen, Avatar, EmojiPicker, SettingsDialog,
        UserProfileDialog, EmojiAvatarPicker
    )
    from styles import (
        GLOBAL_STYLE, SIDEBAR_STYLE, CHAT_AREA_STYLE,
        CHAT_LIST_STYLE, TOP_BAR_STYLE, BOTTOM_BAR_STYLE,
        get_button_style, get_message_input_style,
        COLORS, RADIUS, SPACING, FONT
    )
    from themes import (
        THEMES, get_current_theme, set_theme, set_effect,
        get_current_effect, AnimatedBackground
    )
    from notifications import NotificationManager
    logger.info("All modules imported successfully")
except ImportError as e:
    logger.error(f"Failed to import modules: {e}")
    logger.error(traceback.format_exc())
    sys.exit(1)


class NetworkThread(QThread):
    """Background thread for WebSocket connection"""
    message_received = pyqtSignal(dict)
    connected = pyqtSignal()
    disconnected = pyqtSignal()
    error_occurred = pyqtSignal(str)

    def __init__(self, relay_url, user_id, username, public_key):
        super().__init__()
        self.relay_url = relay_url
        self.user_id = user_id
        self.username = username
        self.public_key = public_key
        self.websocket = None
        self.running = True
        self.loop = None
        self.send_queue = None

    async def send_worker(self):
        """Worker coroutine to send messages from queue"""
        while self.running:
            try:
                message = await asyncio.wait_for(self.send_queue.get(), timeout=1.0)
                if self.websocket and not self.websocket.closed:
                    await self.websocket.send(json.dumps(message))
            except asyncio.TimeoutError:
                continue
            except Exception as e:
                logger.error(f"Error sending message: {e}")

    async def connect_and_listen(self):
        """Connect to relay server and listen for messages"""
        # Initialize send queue in the event loop
        self.send_queue = asyncio.Queue()

        max_retries = 3
        retry_count = 0

        while retry_count < max_retries and self.running:
            try:
                # Create SSL context only for wss:// URLs
                logger.info(f"Attempting connection to: {self.relay_url}")
                ssl_context = None
                if self.relay_url.startswith('wss://'):
                    logger.info("Using SSL context for wss:// connection")
                    ssl_context = ssl.create_default_context()
                    ssl_context.check_hostname = False
                    ssl_context.verify_mode = ssl.CERT_NONE
                else:
                    logger.info(f"No SSL for URL: {self.relay_url}")

                async with websockets.connect(self.relay_url, ssl=ssl_context, ping_interval=30, ping_timeout=10) as websocket:
                    self.websocket = websocket
                    self.connected.emit()
                    retry_count = 0  # Reset on successful connection

                    # Register with server
                    await websocket.send(json.dumps({
                        'type': 'register',
                        'user_id': self.user_id,
                        'username': self.username,
                        'public_key': self.public_key
                    }))

                    # Start send worker
                    send_task = asyncio.create_task(self.send_worker())

                    # Listen for messages
                    try:
                        while self.running:
                            try:
                                message = await asyncio.wait_for(websocket.recv(), timeout=1.0)
                                data = json.loads(message)
                                self.message_received.emit(data)
                            except asyncio.TimeoutError:
                                continue
                            except websockets.exceptions.ConnectionClosed:
                                break
                    finally:
                        send_task.cancel()
                        try:
                            await send_task
                        except asyncio.CancelledError:
                            pass

            except Exception as e:
                logger.error(f"Connection error (attempt {retry_count + 1}/{max_retries}): {e}")
                retry_count += 1
                if retry_count < max_retries:
                    await asyncio.sleep(2)  # Wait before retry
                else:
                    self.error_occurred.emit(str(e))
                    break

        self.disconnected.emit()

    def run(self):
        """Run event loop"""
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        self.loop.run_until_complete(self.connect_and_listen())

    def send_message(self, message):
        """Send message through WebSocket (thread-safe)"""
        if self.loop and self.running:
            try:
                asyncio.run_coroutine_threadsafe(self.send_queue.put(message), self.loop)
            except Exception as e:
                logger.error(f"Error queuing message: {e}")

    def stop(self):
        """Stop the thread"""
        self.running = False


class LoginDialog(QDialog):
    """Modern clean login dialog"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Telegraf - Вход")
        self.setFixedSize(420, 550)

        self.username = None
        self.password = None
        self.user_id = None
        self.db = UserDatabase()
        self.is_register_mode = False
        self.init_ui()

    def init_ui(self):
        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # Container
        container = QWidget()
        container.setStyleSheet(f"""
            QWidget {{
                background: {COLORS['bg_sidebar']};
            }}
        """)

        layout = QVBoxLayout(container)
        layout.setSpacing(SPACING['lg'])
        layout.setContentsMargins(40, 50, 40, 40)

        # Logo
        logo = QLabel("✈️")
        logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo.setStyleSheet(f"font-size: 64px; background: transparent;")
        layout.addWidget(logo)

        # Title
        title = QLabel("Telegraf")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet(f"""
            QLabel {{
                color: {COLORS['text']};
                font-size: 32px;
                font-weight: 600;
                background: transparent;
            }}
        """)
        layout.addWidget(title)

        # Subtitle
        subtitle = QLabel("Современный мессенджер")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setStyleSheet(f"""
            QLabel {{
                color: {COLORS['text_secondary']};
                font-size: 14px;
                background: transparent;
            }}
        """)
        layout.addWidget(subtitle)

        layout.addSpacing(SPACING['xxl'])

        # Username
        self.username_input = ModernInput("Имя пользователя")

        # Load last username
        last_username = self.db.get_last_login()
        if last_username:
            self.username_input.setText(last_username)

        layout.addWidget(self.username_input)

        # Password with show/hide button
        password_container = QWidget()
        password_container.setStyleSheet("background: transparent;")
        password_layout = QHBoxLayout(password_container)
        password_layout.setContentsMargins(0, 0, 0, 0)
        password_layout.setSpacing(SPACING['sm'])

        self.password_input = ModernInput("Пароль")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        password_layout.addWidget(self.password_input)

        # Show/hide password button
        self.show_password_btn = ModernButton("👁", 'icon')
        self.show_password_btn.setFixedSize(45, 45)
        self.show_password_btn.setToolTip("Показать пароль")
        self.show_password_btn.clicked.connect(self.toggle_password_visibility)
        password_layout.addWidget(self.show_password_btn)

        layout.addWidget(password_container)

        # Remember device checkbox
        self.remember_device = QCheckBox("Запомнить это устройство")
        self.remember_device.setChecked(True)
        self.remember_device.setStyleSheet(f"""
            QCheckBox {{
                color: {COLORS['text_secondary']};
                font-size: {FONT['size_sm']}px;
                spacing: {SPACING['sm']}px;
                background: transparent;
            }}
            QCheckBox::indicator {{
                width: 18px;
                height: 18px;
                border-radius: 4px;
                border: 2px solid {COLORS['border']};
                background: {COLORS['bg_input']};
            }}
            QCheckBox::indicator:checked {{
                background: {COLORS['accent']};
                border-color: {COLORS['accent']};
                image: url(data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTIiIGhlaWdodD0iOSIgdmlld0JveD0iMCAwIDEyIDkiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+PHBhdGggZD0iTTEgNEw0LjUgNy41TDExIDEiIHN0cm9rZT0id2hpdGUiIHN0cm9rZS13aWR0aD0iMiIgc3Ryb2tlLWxpbmVjYXA9InJvdW5kIiBzdHJva2UtbGluZWpvaW49InJvdW5kIi8+PC9zdmc+);
            }}
            QCheckBox::indicator:hover {{
                border-color: {COLORS['accent']};
            }}
        """)
        layout.addWidget(self.remember_device)

        layout.addSpacing(SPACING['md'])

        # Error message label
        self.error_label = QLabel("")
        self.error_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.error_label.setStyleSheet(f"""
            QLabel {{
                background: #ef4444;
                color: white;
                padding: {SPACING['md']}px;
                border-radius: {RADIUS['md']}px;
                font-size: 13px;
            }}
        """)
        self.error_label.hide()
        layout.addWidget(self.error_label)

        # Buttons
        self.login_btn = ModernButton("Войти", 'primary')
        self.login_btn.clicked.connect(self.handle_main_button)
        layout.addWidget(self.login_btn)

        self.register_btn = ModernButton("Регистрация", 'secondary')
        self.register_btn.clicked.connect(self.toggle_mode)
        layout.addWidget(self.register_btn)

        main_layout.addWidget(container)

        # Enable enter key
        self.username_input.returnPressed.connect(self.handle_enter)
        self.password_input.returnPressed.connect(self.handle_enter)

    def toggle_password_visibility(self):
        """Toggle password visibility"""
        if self.password_input.echoMode() == QLineEdit.EchoMode.Password:
            self.password_input.setEchoMode(QLineEdit.EchoMode.Normal)
            self.show_password_btn.setText("🙈")
            self.show_password_btn.setToolTip("Скрыть пароль")
        else:
            self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
            self.show_password_btn.setText("👁")
            self.show_password_btn.setToolTip("Показать пароль")

    def handle_main_button(self):
        """Handle main button click (login or register based on mode)"""
        if self.is_register_mode:
            self.register()
        else:
            self.login()

    def toggle_mode(self):
        """Toggle between login and register mode"""
        self.is_register_mode = not self.is_register_mode

        if self.is_register_mode:
            self.login_btn.setText("Зарегистрироваться")
            self.register_btn.setText("Уже есть аккаунт? Войти")
            self.setWindowTitle("Telegraf - Регистрация")
        else:
            self.login_btn.setText("Войти")
            self.register_btn.setText("Регистрация")
            self.setWindowTitle("Telegraf - Вход")

        self.error_label.hide()

    def handle_enter(self):
        """Handle enter key press"""
        if self.is_register_mode:
            self.register()
        else:
            self.login()

    def login(self):
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()

        logger.info(f"Login attempt: username='{username}'")

        if not username or not password:
            logger.warning("Login failed: empty fields")
            self.show_error("Заполните все поля")
            return

        # Check credentials in database
        success, result = self.db.login_user(username, password)

        if success:
            logger.info(f"Login successful: {username}")
            self.username = username
            self.password = password
            self.user_id = result

            # Save last login
            self.db.save_last_login(username)

            # Save session if remember device is checked
            if self.remember_device.isChecked():
                import secrets
                session_token = secrets.token_urlsafe(32)
                self.db.save_session(result, session_token)

                # Save to settings file
                settings_path = Path(__file__).parent.parent / "data" / "settings.json"
                settings_path.parent.mkdir(exist_ok=True)
                import json
                with open(settings_path, 'w', encoding='utf-8') as f:
                    json.dump({'session_token': session_token}, f)

            self.accept()
        else:
            logger.warning(f"Login failed: {result}")
            self.show_error(result)

    def register(self):
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()

        logger.info(f"Registration attempt: username='{username}', password_len={len(password)}")

        if not username or not password:
            logger.warning("Registration failed: empty fields")
            self.show_error("Заполните все поля")
            return

        if len(username) < 3:
            logger.warning(f"Registration failed: username too short ({len(username)} chars)")
            self.show_error("Имя пользователя должно быть минимум 3 символа")
            return

        if len(password) < 4:
            logger.warning(f"Registration failed: password too short ({len(password)} chars)")
            self.show_error("Пароль должен быть минимум 4 символа")
            return

        # Register in database
        logger.info(f"Calling database register for: {username}")
        success, result = self.db.register_user(username, password)

        if success:
            logger.info(f"Registration successful: {username}, user_id={result}")
            self.username = username
            self.password = password
            self.user_id = result

            # Save last login
            self.db.save_last_login(username)

            # Save session if remember device is checked
            if self.remember_device.isChecked():
                import secrets
                session_token = secrets.token_urlsafe(32)
                self.db.save_session(result, session_token)

                # Save to settings file
                settings_path = Path(__file__).parent.parent / "data" / "settings.json"
                settings_path.parent.mkdir(exist_ok=True)
                import json
                with open(settings_path, 'w', encoding='utf-8') as f:
                    json.dump({'session_token': session_token}, f)

            self.show_success("Регистрация успешна! Входим...")
            QTimer.singleShot(1000, self.accept)
        else:
            logger.warning(f"Registration failed: {result}")
            self.show_error(result)

    def show_error(self, message):
        self.error_label.setText(f"❌ {message}")
        self.error_label.setStyleSheet(f"""
            QLabel {{
                background: #ef4444;
                color: white;
                padding: {SPACING['md']}px;
                border-radius: {RADIUS['md']}px;
                font-size: 13px;
            }}
        """)
        self.error_label.show()
        QTimer.singleShot(3000, self.error_label.hide)

    def show_success(self, message):
        self.error_label.setText(f"✅ {message}")
        self.error_label.setStyleSheet(f"""
            QLabel {{
                background: #10b981;
                color: white;
                padding: {SPACING['md']}px;
                border-radius: {RADIUS['md']}px;
                font-size: 13px;
            }}
        """)
        self.error_label.show()


class ChatWidget(QWidget):
    """Modern chat widget"""
    def __init__(self, user_id, username, parent=None):
        super().__init__(parent)
        self.user_id = user_id
        self.username = username
        self.messages = []
        self.emoji_picker = None
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Chat header
        header = QWidget()
        header.setFixedHeight(70)
        header.setStyleSheet(f"""
            QWidget {{
                background: {COLORS['bg_sidebar']};
                border-bottom: 1px solid {COLORS['divider']};
            }}
        """)

        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(SPACING['lg'], SPACING['md'], SPACING['lg'], SPACING['md'])

        # Avatar
        avatar = Avatar(50, self.user_id)
        header_layout.addWidget(avatar)

        # User info
        info_layout = QVBoxLayout()
        info_layout.setSpacing(4)

        name_label = QLabel(self.username)
        name_label.setStyleSheet(f"color: {COLORS['text']}; font-size: 16px; font-weight: 600; background: transparent;")
        info_layout.addWidget(name_label)

        status_label = QLabel("онлайн")
        status_label.setStyleSheet(f"color: {COLORS['online']}; font-size: 13px; background: transparent;")
        info_layout.addWidget(status_label)

        header_layout.addLayout(info_layout)
        header_layout.addStretch()

        layout.addWidget(header)

        # Messages area with scroll
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet(f"""
            QScrollArea {{
                background: {COLORS['bg_chat']};
                border: none;
            }}
        """)

        self.messages_widget = QWidget()
        self.messages_layout = QVBoxLayout(self.messages_widget)
        self.messages_layout.setSpacing(SPACING['sm'])
        self.messages_layout.setContentsMargins(SPACING['lg'], SPACING['lg'], SPACING['lg'], SPACING['lg'])

        # Typing indicator (hidden by default)
        self.typing_indicator = TypingIndicator()
        self.typing_indicator.hide()
        self.messages_layout.addWidget(self.typing_indicator)

        self.messages_layout.addStretch()

        scroll.setWidget(self.messages_widget)
        layout.addWidget(scroll)

        # Input area
        input_container = QWidget()
        input_container.setFixedHeight(70)
        input_container.setStyleSheet(f"""
            QWidget {{
                background: {COLORS['bg_sidebar']};
                border-top: 1px solid {COLORS['divider']};
            }}
        """)

        input_layout = QHBoxLayout(input_container)
        input_layout.setContentsMargins(SPACING['lg'], SPACING['md'], SPACING['lg'], SPACING['md'])
        input_layout.setSpacing(SPACING['sm'])

        # Attach button
        self.attach_btn = ModernButton("📎", 'icon')
        self.attach_btn.setFixedSize(40, 40)
        self.attach_btn.setToolTip("Прикрепить файл")
        input_layout.addWidget(self.attach_btn)

        # Emoji button
        self.emoji_btn = ModernButton("😊", 'icon')
        self.emoji_btn.setFixedSize(40, 40)
        self.emoji_btn.setToolTip("Выбрать эмодзи")
        self.emoji_btn.clicked.connect(self.show_emoji_picker)
        input_layout.addWidget(self.emoji_btn)

        # Message input
        self.message_input = ModernInput("Введите сообщение...")
        self.message_input.setStyleSheet(get_message_input_style())
        input_layout.addWidget(self.message_input)

        # Voice button
        self.voice_btn = ModernButton("🎤", 'icon')
        self.voice_btn.setFixedSize(40, 40)
        self.voice_btn.setToolTip("Голосовое сообщение")
        input_layout.addWidget(self.voice_btn)

        # Send button - beautiful circular button
        self.send_btn = ModernButton("", 'primary')
        self.send_btn.setText("➤")
        self.send_btn.setFixedSize(44, 44)
        self.send_btn.setToolTip("Отправить сообщение")
        self.send_btn.setStyleSheet(f"""
            QPushButton {{
                background: {COLORS['accent']};
                border: none;
                border-radius: 22px;
                color: white;
                font-size: 18px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background: {COLORS['accent_light']};
                transform: scale(1.05);
            }}
            QPushButton:pressed {{
                background: {COLORS['accent_dark']};
                transform: scale(0.95);
            }}
        """)
        input_layout.addWidget(self.send_btn)

        layout.addWidget(input_container)

    def show_emoji_picker(self):
        """Show emoji picker popup"""
        if not self.emoji_picker:
            self.emoji_picker = EmojiPicker(self)
            self.emoji_picker.emoji_selected.connect(self.insert_emoji)

        # Position below emoji button
        btn_pos = self.emoji_btn.mapToGlobal(self.emoji_btn.rect().bottomLeft())
        self.emoji_picker.move(btn_pos.x(), btn_pos.y() - self.emoji_picker.height())
        self.emoji_picker.show()

    def insert_emoji(self, emoji):
        """Insert emoji at cursor position"""
        current_text = self.message_input.text()
        cursor_pos = self.message_input.cursorPosition()
        new_text = current_text[:cursor_pos] + emoji + current_text[cursor_pos:]
        self.message_input.setText(new_text)
        self.message_input.setCursorPosition(cursor_pos + len(emoji))
        self.message_input.setFocus()

    def show_typing_indicator(self):
        """Show typing indicator"""
        self.typing_indicator.show()
        self.scroll_to_bottom()

    def hide_typing_indicator(self):
        """Hide typing indicator"""
        self.typing_indicator.hide()

    def add_message(self, sender, text, is_own=False, timestamp=None, message_type='text', file_path=None, avatar_path=None, is_read=False):
        """Add animated message bubble"""
        if timestamp is None:
            timestamp = datetime.now().strftime("%H:%M")

        bubble = MessageBubble(text, is_own, timestamp, message_type, file_path, avatar_path, is_read)
        # Insert before typing indicator
        insert_index = self.messages_layout.count() - 2  # Before typing indicator and stretch
        self.messages_layout.insertWidget(insert_index, bubble)

        # Auto-scroll
        QTimer.singleShot(100, lambda: self.scroll_to_bottom())

    def scroll_to_bottom(self):
        """Scroll to bottom of messages"""
        scroll = self.findChild(QScrollArea)
        if scroll:
            scroll.verticalScrollBar().setValue(scroll.verticalScrollBar().maximum())


class TelegrafApp(QMainWindow):
    """Modern Telegraf application"""
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Telegraf - Modern Messenger")
        self.setGeometry(100, 100, 1400, 900)

        # Apply modern styles
        self.setStyleSheet(GLOBAL_STYLE)

        # Initialize notification manager
        self.notification_manager = None
        self.notifications_enabled = True  # Notifications enabled by default

        # Animated background
        self.animated_bg = None

        # Pinned chats
        self.pinned_chats = set()

        # Show splash screen
        self.splash = SplashScreen()
        self.splash.show()
        QTimer.singleShot(2000, self.init_after_splash)

    def init_after_splash(self):
        """Initialize after splash screen"""
        logger.info("Closing splash screen...")
        self.splash.close()

        logger.info("Loading configuration...")
        # Load config
        self.load_config()

        logger.info("Initializing encryption...")
        # Initialize encryption
        self.encryption = EncryptionManager()
        self.encryption.generate_keys()

        # User data
        self.user_id = None
        self.username = None
        self.users = {}
        self.chats = {}
        self.current_chat = None
        self.db = UserDatabase()

        # Network
        self.network_thread = None

        logger.info("Showing login dialog...")
        # Show login
        self.show_login()

    def load_config(self):
        """Load configuration with fallback servers"""
        # Handle PyInstaller bundled files
        if getattr(sys, 'frozen', False):
            # Running in PyInstaller bundle
            base_path = Path(sys._MEIPASS)
        else:
            # Running in normal Python
            base_path = Path(__file__).parent.parent

        config_path = base_path / "config" / "config.json"

        logger.info(f"Loading config from: {config_path}")

        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
                self.relay_url = config.get('relay_server', 'ws://localhost:8765')
                self.fallback_servers = config.get('fallback_servers', [])
                logger.info(f"Config loaded. Relay URL: {self.relay_url}")
        except Exception as e:
            logger.error(f"Failed to load config: {e}")
            # Default public server (you should deploy and update this)
            self.relay_url = 'ws://localhost:8765'
            self.fallback_servers = []

        # Load notification settings
        try:
            settings_path = base_path / "data" / "settings.json"
            if settings_path.exists():
                with open(settings_path, 'r', encoding='utf-8') as f:
                    settings = json.load(f)
                    self.notifications_enabled = settings.get('notifications_enabled', True)
                    logger.info(f"Notifications enabled: {self.notifications_enabled}")
        except Exception as e:
            logger.error(f"Failed to load notification settings: {e}")
            self.notifications_enabled = True  # Default to enabled

    def show_login(self):
        """Show login dialog with auto-login support"""
        # Try auto-login first
        import secrets
        settings_path = Path(__file__).parent.parent / "data" / "settings.json"

        if settings_path.exists():
            try:
                import json
                with open(settings_path, 'r', encoding='utf-8') as f:
                    settings = json.load(f)
                    session_token = settings.get('session_token')

                    if session_token:
                        # Try to restore session
                        user_data = self.db.get_session(session_token)
                        if user_data:
                            logger.info(f"Auto-login successful: {user_data['username']}")
                            self.username = user_data['username']
                            self.user_id = user_data['user_id']

                            logger.info("Initializing UI...")
                            self.init_ui()

                            # Initialize notifications
                            logger.info("Creating NotificationManager...")
                            self.notification_manager = NotificationManager(QApplication.instance(), self)
                            logger.info(f"NotificationManager created: {self.notification_manager is not None}")
                            if self.notification_manager and self.notification_manager.tray_icon:
                                logger.info(f"Tray icon visible: {self.notification_manager.tray_icon.isVisible()}")
                            else:
                                logger.warning("NotificationManager or tray_icon is None!")

                            logger.info("Connecting to server...")
                            self.connect_to_server()
                            logger.info("Showing main window...")
                            self.show()
                            return
            except Exception as e:
                logger.error(f"Auto-login failed: {e}")

        # Show login dialog if auto-login failed
        logger.info("Creating login dialog...")
        try:
            dialog = LoginDialog(self)
            logger.info("Login dialog created successfully")
        except Exception as e:
            logger.error(f"Failed to create login dialog: {e}")
            import traceback
            logger.error(traceback.format_exc())
            sys.exit(1)

        logger.info("Showing login dialog...")
        try:
            result = dialog.exec()
            logger.info(f"Login dialog result: {result}")
            logger.info(f"Dialog accepted: {result == QDialog.DialogCode.Accepted}")
        except Exception as e:
            logger.error(f"Error showing dialog: {e}")
            import traceback
            logger.error(traceback.format_exc())
            sys.exit(1)

        if result == QDialog.DialogCode.Accepted:
            logger.info(f"User logged in: {dialog.username}")

            self.username = dialog.username
            self.user_id = dialog.user_id

            logger.info("Initializing UI...")
            self.init_ui()

            # Initialize notifications
            logger.info("Creating NotificationManager...")
            self.notification_manager = NotificationManager(QApplication.instance(), self)
            logger.info(f"NotificationManager created: {self.notification_manager is not None}")
            if self.notification_manager and self.notification_manager.tray_icon:
                logger.info(f"Tray icon visible: {self.notification_manager.tray_icon.isVisible()}")
            else:
                logger.warning("NotificationManager or tray_icon is None!")

            logger.info("Connecting to server...")
            self.connect_to_server()
            logger.info("Showing main window...")
            self.show()
            self.raise_()
            self.activateWindow()
            logger.info("Main window should be visible now")
        else:
            logger.info("Login cancelled, exiting...")
            sys.exit()

    def init_ui(self):
        """Initialize modern UI"""
        # Central widget
        central = QWidget()
        central.setStyleSheet(f"""
            QWidget {{
                background: {COLORS['bg_app']};
            }}
        """)
        self.setCentralWidget(central)

        layout = QVBoxLayout(central)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Animated background
        self.animated_bg = AnimatedBackground(central)
        self.animated_bg.setGeometry(central.rect())
        self.animated_bg.lower()

        # Top bar
        self.init_top_bar(layout)

        # Main content
        content_layout = QHBoxLayout()
        content_layout.setSpacing(0)

        # Sidebar
        self.init_sidebar(content_layout)

        # Chat area
        self.chat_stack = QStackedWidget()
        self.chat_stack.setStyleSheet(f"background: {COLORS['bg_chat']};")
        content_layout.addWidget(self.chat_stack, stretch=3)

        # Welcome screen
        welcome = QLabel("Выберите чат для начала общения")
        welcome.setAlignment(Qt.AlignmentFlag.AlignCenter)
        welcome.setStyleSheet(f"""
            QLabel {{
                color: {COLORS['text_muted']};
                font-size: 18px;
                background: transparent;
            }}
        """)
        self.chat_stack.addWidget(welcome)

        layout.addLayout(content_layout)

    def init_top_bar(self, parent_layout):
        """Modern top bar"""
        top_bar = QWidget()
        top_bar.setFixedHeight(50)
        top_bar.setStyleSheet(f"""
            QWidget {{
                background: {COLORS['bg_sidebar']};
                border-bottom: 1px solid {COLORS['divider']};
            }}
        """)

        layout = QHBoxLayout(top_bar)
        layout.setContentsMargins(SPACING['lg'], 0, SPACING['lg'], 0)

        # App title
        title = QLabel("Telegraf")
        title.setStyleSheet(f"color: {COLORS['text']}; font-size: 16px; font-weight: 600; background: transparent;")
        layout.addWidget(title)

        layout.addStretch()

        # Connection status
        self.connection_status = ConnectionStatus()
        layout.addWidget(self.connection_status)

        parent_layout.addWidget(top_bar)

    def init_sidebar(self, parent_layout):
        """Initialize modern sidebar"""
        sidebar = QWidget()
        sidebar.setFixedWidth(350)
        sidebar.setStyleSheet(SIDEBAR_STYLE)

        layout = QVBoxLayout(sidebar)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # User profile header
        profile = QWidget()
        profile.setFixedHeight(80)
        profile.setStyleSheet(f"""
            QWidget {{
                background: {COLORS['bg_sidebar']};
                border-bottom: 1px solid {COLORS['divider']};
            }}
        """)

        profile_layout = QHBoxLayout(profile)
        profile_layout.setContentsMargins(SPACING['lg'], SPACING['md'], SPACING['lg'], SPACING['md'])
        profile_layout.setSpacing(SPACING['md'])

        # Avatar
        self.user_avatar = Avatar(50, self.user_id)
        profile_layout.addWidget(self.user_avatar)

        # User info
        user_info = QVBoxLayout()
        user_info.setSpacing(4)

        name = QLabel(self.username if hasattr(self, 'username') else "User")
        name.setStyleSheet(f"color: {COLORS['text']}; font-size: 15px; font-weight: 600; background: transparent;")
        user_info.addWidget(name)

        status = QLabel("в сети")
        status.setStyleSheet(f"color: {COLORS['online']}; font-size: 13px; background: transparent;")
        user_info.addWidget(status)

        profile_layout.addLayout(user_info)
        profile_layout.addStretch()

        # Settings button
        settings_btn = ModernButton("⚙️", 'icon')
        settings_btn.setFixedSize(36, 36)
        settings_btn.setToolTip("Настройки")
        settings_btn.clicked.connect(self.show_settings)
        profile_layout.addWidget(settings_btn)

        # Logout button
        logout_btn = ModernButton("🚪", 'icon')
        logout_btn.setFixedSize(36, 36)
        logout_btn.setToolTip("Выйти из аккаунта")
        logout_btn.clicked.connect(self.logout)
        profile_layout.addWidget(logout_btn)

        layout.addWidget(profile)

        # Search bar
        search = SearchBar()
        search.textChanged.connect(self.filter_chats)
        layout.addWidget(search)

        # Chats list
        self.chats_list = QListWidget()
        self.chats_list.setStyleSheet(CHAT_LIST_STYLE)
        layout.addWidget(self.chats_list)

        parent_layout.addWidget(sidebar)

    def show_settings(self):
        """Show settings dialog"""
        try:
            logger.info("Opening settings dialog...")
            dialog = SettingsDialog(self.user_id, self.username, self.db, self)
            logger.info("Settings dialog created")
            result = dialog.exec()
            logger.info(f"Settings dialog closed with result: {result}")

            if result == QDialog.DialogCode.Accepted:
                # Update profile if changed
                new_username = dialog.username_input.text().strip()
                if new_username and new_username != self.username:
                    self.username = new_username
                    # Update UI
                    for i in range(self.user_avatar.parent().layout().count()):
                        widget = self.user_avatar.parent().layout().itemAt(i).widget()
                        if isinstance(widget, QLabel) and widget.text() != "в сети":
                            widget.setText(new_username)
                            break
        except Exception as e:
            logger.error(f"Error in settings dialog: {e}")
            import traceback
            logger.error(traceback.format_exc())
            QMessageBox.critical(self, "Ошибка", f"Не удалось открыть настройки:\n{str(e)}")

    def refresh_theme(self):
        """Refresh UI with new theme colors"""
        try:
            logger.info("Refreshing theme...")
            # Reload styles
            from styles import COLORS, GLOBAL_STYLE, SIDEBAR_STYLE, CHAT_AREA_STYLE

            # Update main window stylesheet
            self.setStyleSheet(GLOBAL_STYLE)

            # Update central widget
            if self.centralWidget():
                self.centralWidget().setStyleSheet(f"QWidget {{ background: {COLORS['bg_app']}; }}")

            # Update chat stack
            if hasattr(self, 'chat_stack'):
                self.chat_stack.setStyleSheet(f"background: {COLORS['bg_chat']};")

            logger.info("Theme refreshed successfully")
        except Exception as e:
            logger.error(f"Error refreshing theme: {e}")
            import traceback
            logger.error(traceback.format_exc())

    def filter_chats(self, text):
        """Filter chat list by search text"""
        search_text = text.lower()
        for i in range(self.chats_list.count()):
            item = self.chats_list.item(i)
            widget = self.chats_list.itemWidget(item)
            if hasattr(widget, 'username'):
                visible = search_text in widget.username.lower()
                item.setHidden(not visible)

    def connect_to_server(self):
        """Connect to relay server with fallback"""
        public_key = self.encryption.get_public_key_pem()

        self.network_thread = NetworkThread(
            self.relay_url,
            self.user_id,
            self.username,
            public_key
        )
        self.network_thread.message_received.connect(self.handle_message)
        self.network_thread.connected.connect(self.on_connected)
        self.network_thread.disconnected.connect(self.on_disconnected)
        self.network_thread.error_occurred.connect(self.on_error)
        self.network_thread.start()

    def on_connected(self):
        """Handle successful connection"""
        self.connection_status.set_status(True)

    def on_disconnected(self):
        """Handle disconnection"""
        self.connection_status.set_status(False)

    def on_error(self, error):
        """Handle connection error"""
        self.connection_status.set_status(False)
        # Try fallback servers
        if self.fallback_servers:
            self.relay_url = self.fallback_servers.pop(0)
            QTimer.singleShot(2000, self.connect_to_server)

    def handle_message(self, data):
        """Handle incoming message"""
        msg_type = data.get('type')

        if msg_type == 'user_list':
            self.update_user_list(data.get('users', []))

        elif msg_type == 'user_online':
            self.add_user(data.get('user_id'), data.get('username'))

        elif msg_type == 'user_offline':
            self.update_user_status(data.get('user_id'), 'offline')

        elif msg_type == 'message':
            self.receive_message(data)

        elif msg_type == 'typing':
            # Show typing indicator
            sender_id = data.get('from')
            if sender_id in self.chats:
                self.chats[sender_id].show_typing_indicator()
                # Hide after 3 seconds
                QTimer.singleShot(3000, lambda: self.chats[sender_id].hide_typing_indicator())

        elif msg_type == 'public_key':
            user_id = data.get('user_id')
            public_key = data.get('public_key')
            self.encryption.load_peer_public_key(user_id, public_key)

    def update_user_list(self, users):
        """Update list of online users"""
        for user in users:
            user_id = user.get('user_id')
            username = user.get('username')
            public_key = user.get('public_key')

            self.add_user(user_id, username)

            if public_key:
                self.encryption.load_peer_public_key(user_id, public_key)

        # Auto-open last chat if exists
        last_chat_id = self.db.get_last_chat(self.user_id)
        if last_chat_id and last_chat_id in self.users:
            QTimer.singleShot(500, lambda: self.open_chat(last_chat_id))

    def add_user(self, user_id, username):
        """Add user to list with animation"""
        if user_id not in self.users:
            self.users[user_id] = {'username': username, 'status': 'online'}

            # Get avatar path
            avatar_path = self.db.get_avatar(user_id)

            # Create user item
            item = QListWidgetItem(self.chats_list)
            user_widget = UserListItem(user_id, username, avatar_path=avatar_path)
            user_widget.clicked.connect(self.open_chat)
            user_widget.pin_toggled.connect(self.toggle_pin_chat)
            user_widget.profile_requested.connect(self.show_user_profile)

            item.setSizeHint(user_widget.sizeHint())
            self.chats_list.setItemWidget(item, user_widget)

            # Request public key
            if self.network_thread:
                self.network_thread.send_message({
                    'type': 'get_public_key',
                    'user_id': user_id
                })

    def toggle_pin_chat(self, user_id, is_pinned):
        """Toggle chat pin status"""
        try:
            logger.info(f"Toggling pin for user {user_id}: {is_pinned}")
            if is_pinned:
                self.pinned_chats.add(user_id)
            else:
                self.pinned_chats.discard(user_id)

            # Update widget pin indicator
            for i in range(self.chats_list.count()):
                item = self.chats_list.item(i)
                widget = self.chats_list.itemWidget(item)
                if widget and hasattr(widget, 'user_id') and widget.user_id == user_id:
                    widget.is_pinned = is_pinned
                    if hasattr(widget, 'update_pin_indicator'):
                        widget.update_pin_indicator()
                    logger.info(f"Updated pin indicator for {user_id}")
                    break

            # Re-sort chat list
            self.sort_chat_list()
            logger.info("Pin toggled successfully")
        except Exception as e:
            logger.error(f"Error toggling pin: {e}")
            import traceback
            logger.error(traceback.format_exc())

    def sort_chat_list(self):
        """Sort chat list - pinned chats first"""
        try:
            logger.info(f"Starting sort_chat_list, pinned chats: {self.pinned_chats}")

            # Don't sort if list is empty or has only one item
            if self.chats_list.count() <= 1:
                logger.info("List has 0 or 1 items, skipping sort")
                return

            # Collect user data instead of widgets
            items_data = []
            for i in range(self.chats_list.count()):
                item = self.chats_list.item(i)
                widget = self.chats_list.itemWidget(item)
                if widget and hasattr(widget, 'user_id'):
                    items_data.append({
                        'user_id': widget.user_id,
                        'username': getattr(widget, 'username', ''),
                        'status': getattr(widget, 'status', 'offline'),
                        'avatar_path': getattr(widget, 'avatar_path', None),
                        'last_message': getattr(widget, 'last_message', ''),
                        'unread_count': getattr(widget, 'unread_count', 0),
                        'is_pinned': widget.user_id in self.pinned_chats
                    })
                    logger.info(f"Collected data: user_id={widget.user_id}, username={items_data[-1]['username']}")

            logger.info(f"Total items collected: {len(items_data)}")

            # Sort: pinned first, then by username
            def sort_key(data):
                return (not data['is_pinned'], data['username'].lower())

            items_data.sort(key=sort_key)
            logger.info("Data sorted successfully")

            # Clear and recreate widgets
            logger.info("Clearing chat list...")
            self.chats_list.clear()
            logger.info("Chat list cleared")

            # Recreate widgets from data
            logger.info("Recreating widgets...")
            for idx, data in enumerate(items_data):
                item = QListWidgetItem(self.chats_list)
                widget = UserListItem(
                    data['user_id'],
                    data['username'],
                    data['status'],
                    data['avatar_path'],
                    data['last_message'],
                    data['unread_count'],
                    data['is_pinned']
                )
                widget.clicked.connect(self.open_chat)
                widget.pin_toggled.connect(self.toggle_pin_chat)
                widget.profile_requested.connect(self.show_user_profile)

                item.setSizeHint(widget.sizeHint())
                self.chats_list.setItemWidget(item, widget)
                logger.info(f"Recreated widget {idx}: {data['username']}")

            logger.info("Sort completed successfully")
        except Exception as e:
            logger.error(f"Error sorting chat list: {e}")
            import traceback
            logger.error(traceback.format_exc())

    def show_user_profile(self, user_id):
        """Show user profile dialog"""
        if user_id in self.users:
            username = self.users[user_id]['username']
            dialog = UserProfileDialog(user_id, username, self.db, self)
            dialog.exec()

    def update_user_status(self, user_id, status):
        """Update user status"""
        if user_id in self.users:
            self.users[user_id]['status'] = status

            # Update UI
            for i in range(self.chats_list.count()):
                item = self.chats_list.item(i)
                widget = self.chats_list.itemWidget(item)
                if hasattr(widget, 'user_id') and widget.user_id == user_id:
                    widget.set_status(status)
                    break

    def open_chat(self, user_id):
        """Open chat with smooth transition"""
        username = self.users[user_id]['username']

        if user_id not in self.chats:
            chat = ChatWidget(user_id, username)
            chat.send_btn.clicked.connect(lambda: self.send_message(user_id))
            chat.message_input.returnPressed.connect(lambda: self.send_message(user_id))
            chat.message_input.textChanged.connect(lambda: self.on_message_input_changed(user_id))
            chat.attach_btn.clicked.connect(lambda: self.attach_file(user_id))
            chat.voice_btn.clicked.connect(lambda: self.record_voice(user_id))

            self.chats[user_id] = chat
            self.chat_stack.addWidget(chat)

            # Load message history
            self.load_message_history(user_id)

        self.current_chat = user_id
        self.chat_stack.setCurrentWidget(self.chats[user_id])

        # Save as last opened chat
        self.db.save_last_chat(self.user_id, user_id)

    def attach_file(self, recipient_id):
        """Attach and send file"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Выберите файл",
            "",
            "Images (*.png *.jpg *.jpeg *.gif *.bmp);;All Files (*.*)"
        )

        if file_path:
            # Get install directory for saving files
            if getattr(sys, 'frozen', False):
                install_dir = Path(sys.executable).parent
            else:
                install_dir = Path(__file__).parent.parent

            files_dir = install_dir / "data" / "files"
            files_dir.mkdir(parents=True, exist_ok=True)

            # Copy file to data folder
            import shutil
            file_name = Path(file_path).name
            dest_path = files_dir / f"{self.user_id}_{datetime.now().timestamp()}_{file_name}"
            shutil.copy2(file_path, dest_path)

            # Send file message
            chat = self.chats[recipient_id]

            # Determine message type
            file_ext = Path(file_path).suffix.lower()
            if file_ext in ['.png', '.jpg', '.jpeg', '.gif', '.bmp']:
                message_type = 'file'
            else:
                message_type = 'file'

            # Add to chat
            chat.add_message(self.username, file_name, is_own=True, message_type=message_type, file_path=str(dest_path))

            # Send through network (simplified - just send filename)
            encrypted = self.encryption.encrypt_message(f"[FILE:{file_name}]", recipient_id)
            if encrypted:
                self.network_thread.send_message({
                    'type': 'message',
                    'from': self.user_id,
                    'to': recipient_id,
                    'content': encrypted,
                    'encrypted': True,
                    'message_type': message_type,
                    'file_path': str(dest_path)
                })

            # Save to database
            self.db.save_message(self.user_id, recipient_id, f"[FILE:{file_name}]", is_own=True)

    def record_voice(self, recipient_id):
        """Record and send voice message (placeholder)"""
        # This is a placeholder - full voice recording would require PyAudio
        chat = self.chats[recipient_id]
        QMessageBox.information(
            self,
            "Голосовые сообщения",
            "Функция записи голосовых сообщений будет добавлена в следующей версии.\n\nДля полной реализации требуется установка PyAudio."
        )

    def send_message(self, recipient_id):
        """Send encrypted message"""
        if recipient_id not in self.chats:
            return

        chat = self.chats[recipient_id]
        text = chat.message_input.text().strip()

        if not text:
            return

        # Encrypt message
        encrypted = self.encryption.encrypt_message(text, recipient_id)

        if encrypted:
            # Send encrypted message
            self.network_thread.send_message({
                'type': 'message',
                'from': self.user_id,
                'to': recipient_id,
                'content': encrypted,
                'encrypted': True,
                'message_type': 'text'
            })

            # Get user avatar
            avatar_path = self.db.get_avatar(self.user_id)

            # Add to chat (only once)
            timestamp = datetime.now().strftime("%H:%M")
            chat.add_message(self.username, text, is_own=True, timestamp=timestamp, avatar_path=avatar_path, is_read=False)
            chat.message_input.clear()

            # Save to database
            self.db.save_message(self.user_id, recipient_id, text, is_own=True)

    def on_message_input_changed(self, recipient_id):
        """Handle message input change - send typing indicator"""
        if recipient_id in self.chats:
            # Send typing notification to server
            self.network_thread.send_message({
                'type': 'typing',
                'from': self.user_id,
                'to': recipient_id
            })

    def receive_message(self, data):
        """Receive and decrypt message"""
        sender_id = data.get('from')
        sender_username = data.get('from_username')
        encrypted = data.get('encrypted', False)
        content = data.get('content')
        message_type = data.get('message_type', 'text')
        file_path = data.get('file_path')

        # Decrypt if encrypted
        if encrypted:
            text = self.encryption.decrypt_message(content)
            if not text:
                text = "[Не удалось расшифровать]"
        else:
            text = content

        # Add to chat (only if not from self to prevent duplication)
        if sender_id != self.user_id:
            if sender_id not in self.chats:
                # Auto-open chat
                for i in range(self.chats_list.count()):
                    item = self.chats_list.item(i)
                    widget = self.chats_list.itemWidget(item)
                    if hasattr(widget, 'user_id') and widget.user_id == sender_id:
                        self.open_chat(sender_id)
                        break

            if sender_id in self.chats:
                # Get sender avatar
                avatar_path = self.db.get_avatar(sender_id)

                # Hide typing indicator
                self.chats[sender_id].hide_typing_indicator()

                timestamp = datetime.now().strftime("%H:%M")
                self.chats[sender_id].add_message(
                    sender_username, text, is_own=False, timestamp=timestamp,
                    message_type=message_type, file_path=file_path, avatar_path=avatar_path
                )

                # Save to database
                self.db.save_message(sender_id, self.user_id, text, is_own=False)

                # Show notification if window is not active and notifications enabled
                if not self.isActiveWindow() and self.notification_manager and self.notifications_enabled:
                    logger.info(f"Showing notification for message from {sender_username}")
                    self.notification_manager.show_message_notification(sender_username, text)
                elif not self.notifications_enabled:
                    logger.info("Notification skipped - notifications disabled")

    def load_message_history(self, user_id):
        """Load message history from database"""
        messages = self.db.get_messages(self.user_id, user_id)

        if user_id in self.chats:
            chat = self.chats[user_id]
            for msg in messages:
                from_user, to_user, content, timestamp, is_own = msg
                # Parse timestamp
                try:
                    dt = datetime.fromisoformat(timestamp)
                    time_str = dt.strftime("%H:%M")
                except:
                    time_str = None
                chat.add_message("", content, is_own=bool(is_own), timestamp=time_str)

    def logout(self):
        """Logout user and return to login screen"""
        reply = QMessageBox.question(
            self,
            'Выход',
            'Вы уверены, что хотите выйти?',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            # Clear session
            if hasattr(self, 'user_id'):
                self.db.clear_session(self.user_id)

            # Clear session file
            settings_path = Path(__file__).parent.parent / "data" / "settings.json"
            if settings_path.exists():
                import json
                with open(settings_path, 'w', encoding='utf-8') as f:
                    json.dump({}, f)

            # Stop network thread
            if self.network_thread:
                self.network_thread.stop()
                self.network_thread.wait()

            # Close and restart
            self.close()
            QApplication.quit()
            import subprocess
            subprocess.Popen([sys.executable] + sys.argv)

    def closeEvent(self, event):
        """Handle window close"""
        if self.network_thread:
            self.network_thread.stop()
            self.network_thread.wait()
        event.accept()


def main():
    """Main application entry point with error handling"""
    try:
        logger.info("Initializing Qt Application...")
        app = QApplication(sys.argv)
        app.setStyle('Fusion')

        # Set app-wide font
        font = QFont("Segoe UI", 10)
        app.setFont(font)

        logger.info("Creating main window...")
        window = TelegrafApp()

        logger.info("Starting event loop...")
        sys.exit(app.exec())

    except Exception as e:
        logger.error(f"Fatal error: {e}")
        logger.error(traceback.format_exc())

        # Show error dialog if possible
        try:
            error_app = QApplication.instance()
            if error_app is None:
                error_app = QApplication(sys.argv)

            QMessageBox.critical(
                None,
                "Telegraf Error",
                f"Fatal error occurred:\n\n{str(e)}\n\nCheck logs/telegraf_*.log for details"
            )
        except:
            print(f"FATAL ERROR: {e}", file=sys.stderr)
            print(traceback.format_exc(), file=sys.stderr)

        sys.exit(1)


if __name__ == '__main__':
    main()
