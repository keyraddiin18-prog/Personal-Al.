import sqlite3
from pathlib import Path
from datetime import datetime


# ==========================================
# KEYRADDIIN PERSONAL AI V2.0
# SQLITE DATABASE SYSTEM
# ==========================================

BASE_DIR = Path(__file__).resolve().parent.parent

DATABASE_DIR = BASE_DIR / "database"

DATABASE_DIR.mkdir(parents=True, exist_ok=True)

DB_PATH = DATABASE_DIR / "keyraddiin_ai.db"


# ==========================================
# DATABASE CONNECTION
# ==========================================

def get_connection():

    connection = sqlite3.connect(
        DB_PATH,
        timeout=30
    )

    connection.row_factory = sqlite3.Row

    # Enable foreign keys
    connection.execute(
        "PRAGMA foreign_keys = ON"
    )

    return connection


# ==========================================
# INITIALIZE DATABASE
# ==========================================

def init_db():

    with get_connection() as conn:

        cursor = conn.cursor()

        # CHAT SESSIONS
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS chats (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                title TEXT NOT NULL,

                created_at TEXT NOT NULL,

                updated_at TEXT NOT NULL

            )
        """)

        # CHAT MESSAGES
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS messages (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                chat_id INTEGER NOT NULL,

                role TEXT NOT NULL,

                content TEXT NOT NULL,

                created_at TEXT NOT NULL,

                FOREIGN KEY(chat_id)
                REFERENCES chats(id)
                ON DELETE CASCADE

            )
        """)

        # USER SETTINGS
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS settings (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                setting_key TEXT UNIQUE NOT NULL,

                setting_value TEXT

            )
        """)

        conn.commit()

    print("DATABASE INITIALIZED!")


# ==========================================
# CREATE NEW CHAT
# ==========================================

def create_chat(title="New Chat"):

    now = datetime.now().isoformat()

    with get_connection() as conn:

        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO chats
            (title, created_at, updated_at)

            VALUES (?, ?, ?)
        """, (title, now, now))

        return cursor.lastrowid


# ==========================================
# SAVE MESSAGE
# ==========================================

def save_message(chat_id, role, content):

    if role not in ("user", "assistant"):

        raise ValueError("Invalid message role")

    if not content or not str(content).strip():

        return False

    now = datetime.now().isoformat()

    with get_connection() as conn:

        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO messages
            (chat_id, role, content, created_at)

            VALUES (?, ?, ?, ?)
        """, (
            chat_id,
            role,
            str(content),
            now
        ))

        cursor.execute("""
            UPDATE chats
            SET updated_at = ?
            WHERE id = ?
        """, (now, chat_id))

        return cursor.lastrowid


# ==========================================
# GET CHAT HISTORY
# ==========================================

def get_chat_history(chat_id):

    with get_connection() as conn:

        cursor = conn.cursor()

        cursor.execute("""
            SELECT *
            FROM messages
            WHERE chat_id = ?
            ORDER BY id ASC
        """, (chat_id,))

        return [
            dict(row)
            for row in cursor.fetchall()
        ]


# ==========================================
# GET ALL CHATS
# ==========================================

def get_all_chats():

    with get_connection() as conn:

        cursor = conn.cursor()

        cursor.execute("""
            SELECT *
            FROM chats
            ORDER BY updated_at DESC
        """)

        return [
            dict(row)
            for row in cursor.fetchall()
        ]


# ==========================================
# DELETE CHAT
# ==========================================

def delete_chat(chat_id):

    with get_connection() as conn:

        cursor = conn.cursor()

        cursor.execute("""
            DELETE FROM chats
            WHERE id = ?
        """, (chat_id,))

        return cursor.rowcount > 0


# ==========================================
# SAVE USER SETTING
# ==========================================

def save_setting(key, value):

    if not key:

        return False

    with get_connection() as conn:

        conn.execute("""
            INSERT INTO settings
            (setting_key, setting_value)

            VALUES (?, ?)

            ON CONFLICT(setting_key)

            DO UPDATE SET
            setting_value = excluded.setting_value

        """, (str(key), str(value)))

        return True


# ==========================================
# GET USER SETTING
# ==========================================

def get_setting(key, default=None):

    with get_connection() as conn:

        cursor = conn.cursor()

        cursor.execute("""
            SELECT setting_value
            FROM settings
            WHERE setting_key = ?
        """, (str(key),))

        result = cursor.fetchone()

        if result:

            return result["setting_value"]

        return default


# ==========================================
# DELETE USER SETTING
# ==========================================

def delete_setting(key):

    with get_connection() as conn:

        cursor = conn.cursor()

        cursor.execute("""
            DELETE FROM settings
            WHERE setting_key = ?
        """, (str(key),))

        return cursor.rowcount > 0


# ==========================================
# DATABASE INFORMATION
# ==========================================

def database_info():

    with get_connection() as conn:

        total_chats = conn.execute("""
            SELECT COUNT(*)
            FROM chats
        """).fetchone()[0]

        total_messages = conn.execute("""
            SELECT COUNT(*)
            FROM messages
        """).fetchone()[0]

        total_settings = conn.execute("""
            SELECT COUNT(*)
            FROM settings
        """).fetchone()[0]

        return {

            "database": "KEYRADDIIN PERSONAL AI",

            "version": "2.0",

            "status": "connected",

            "total_chats": total_chats,

            "total_messages": total_messages,

            "total_settings": total_settings,

            "storage": "SQLite"

        }


# ==========================================
# INITIALIZE DATABASE AUTOMATICALLY
# ==========================================

init_db()


print("KEYRADDIIN SQLITE DATABASE SYSTEM LOADED!")