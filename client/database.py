"""
User Database Manager
Handles user registration and authentication
"""
import sqlite3
import hashlib
import os
from pathlib import Path
from datetime import datetime

class UserDatabase:
    def __init__(self):
        # Database in data folder
        self.db_path = Path(__file__).parent.parent / "data" / "users.db"
        self.db_path.parent.mkdir(exist_ok=True)
        self.init_database()

    def init_database(self):
        """Initialize database with users table"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id TEXT PRIMARY KEY,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                created_at TEXT NOT NULL,
                last_login TEXT
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                from_user_id TEXT NOT NULL,
                to_user_id TEXT NOT NULL,
                content TEXT NOT NULL,
                encrypted BOOLEAN DEFAULT 1,
                timestamp TEXT NOT NULL,
                is_own BOOLEAN DEFAULT 0
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS chat_settings (
                user_id TEXT PRIMARY KEY,
                last_chat_user_id TEXT,
                last_opened TEXT
            )
        """)

        conn.commit()
        conn.close()

    def hash_password(self, password):
        """Hash password with SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()

    def register_user(self, username, password):
        """Register new user"""
        if not username or not password:
            return False, "Имя пользователя и пароль обязательны"

        if len(username) < 3:
            return False, "Имя пользователя должно быть минимум 3 символа"

        if len(password) < 4:
            return False, "Пароль должен быть минимум 4 символа"

        password_hash = self.hash_password(password)
        user_id = hashlib.sha256(f"{username}{password}".encode()).hexdigest()[:16]

        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO users (user_id, username, password_hash, created_at)
                VALUES (?, ?, ?, ?)
            """, (user_id, username, password_hash, datetime.now().isoformat()))

            conn.commit()
            conn.close()

            return True, user_id

        except sqlite3.IntegrityError:
            return False, "Пользователь с таким именем уже существует"
        except Exception as e:
            return False, f"Ошибка регистрации: {str(e)}"

    def login_user(self, username, password):
        """Login existing user"""
        if not username or not password:
            return False, "Введите имя пользователя и пароль"

        password_hash = self.hash_password(password)

        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cursor.execute("""
                SELECT user_id FROM users
                WHERE username = ? AND password_hash = ?
            """, (username, password_hash))

            result = cursor.fetchone()

            if result:
                user_id = result[0]

                # Update last login
                cursor.execute("""
                    UPDATE users SET last_login = ?
                    WHERE user_id = ?
                """, (datetime.now().isoformat(), user_id))

                conn.commit()
                conn.close()

                return True, user_id
            else:
                conn.close()
                return False, "Неверное имя пользователя или пароль"

        except Exception as e:
            return False, f"Ошибка входа: {str(e)}"

    def user_exists(self, username):
        """Check if username exists"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cursor.execute("SELECT 1 FROM users WHERE username = ?", (username,))
            result = cursor.fetchone()

            conn.close()
            return result is not None

        except:
            return False

    def save_message(self, from_user_id, to_user_id, content, is_own=False):
        """Save message to database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO messages (from_user_id, to_user_id, content, timestamp, is_own)
                VALUES (?, ?, ?, ?, ?)
            """, (from_user_id, to_user_id, content, datetime.now().isoformat(), is_own))

            conn.commit()
            conn.close()
            return True

        except Exception as e:
            print(f"Error saving message: {e}")
            return False

    def get_messages(self, user_id, other_user_id, limit=100):
        """Get message history between two users"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cursor.execute("""
                SELECT from_user_id, to_user_id, content, timestamp, is_own
                FROM messages
                WHERE (from_user_id = ? AND to_user_id = ?)
                   OR (from_user_id = ? AND to_user_id = ?)
                ORDER BY timestamp ASC
                LIMIT ?
            """, (user_id, other_user_id, other_user_id, user_id, limit))

            messages = cursor.fetchall()
            conn.close()

            return messages

        except Exception as e:
            print(f"Error getting messages: {e}")
            return []

    def save_last_chat(self, user_id, last_chat_user_id):
        """Save last opened chat"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cursor.execute("""
                INSERT OR REPLACE INTO chat_settings (user_id, last_chat_user_id, last_opened)
                VALUES (?, ?, ?)
            """, (user_id, last_chat_user_id, datetime.now().isoformat()))

            conn.commit()
            conn.close()
            return True

        except Exception as e:
            print(f"Error saving last chat: {e}")
            return False

    def get_last_chat(self, user_id):
        """Get last opened chat"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cursor.execute("""
                SELECT last_chat_user_id FROM chat_settings
                WHERE user_id = ?
            """, (user_id,))

            result = cursor.fetchone()
            conn.close()

            return result[0] if result else None

        except Exception as e:
            print(f"Error getting last chat: {e}")
            return None

    def save_last_login(self, username):
        """Save last logged in username"""
        try:
            settings_path = self.db_path.parent / "settings.json"
            import json

            settings = {}
            if settings_path.exists():
                with open(settings_path, 'r', encoding='utf-8') as f:
                    settings = json.load(f)

            settings['last_username'] = username

            with open(settings_path, 'w', encoding='utf-8') as f:
                json.dump(settings, f, ensure_ascii=False, indent=2)

            return True

        except Exception as e:
            print(f"Error saving last login: {e}")
            return False

    def get_last_login(self):
        """Get last logged in username"""
        try:
            settings_path = self.db_path.parent / "settings.json"
            import json

            if settings_path.exists():
                with open(settings_path, 'r', encoding='utf-8') as f:
                    settings = json.load(f)
                    return settings.get('last_username')

            return None

        except Exception as e:
            print(f"Error getting last login: {e}")
            return None
