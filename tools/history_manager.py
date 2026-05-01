# tools/history_manager.py
# Manages persistent conversation history using SQLite.

import sqlite3
import json
import os
from datetime import datetime

DB_PATH = "legal_chat_history.db"

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Create tables if they don't exist."""
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                created_at TEXT NOT NULL,
                last_updated TEXT NOT NULL
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id INTEGER NOT NULL,
                role TEXT NOT NULL,
                content TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                FOREIGN KEY (session_id) REFERENCES sessions(id)
            )
        """)
        conn.commit()

def create_session(title: str) -> int:
    """Create a new chat session and return its ID."""
    now = datetime.now().isoformat()
    with get_connection() as conn:
        cursor = conn.execute(
            "INSERT INTO sessions (title, created_at, last_updated) VALUES (?, ?, ?)",
            (title, now, now)
        )
        conn.commit()
        return cursor.lastrowid

def save_message(session_id: int, role: str, content: str):
    """Save a message to a session."""
    now = datetime.now().isoformat()
    with get_connection() as conn:
        conn.execute(
            "INSERT INTO messages (session_id, role, content, timestamp) VALUES (?, ?, ?, ?)",
            (session_id, role, content, now)
        )
        conn.execute(
            "UPDATE sessions SET last_updated = ? WHERE id = ?",
            (now, session_id)
        )
        conn.commit()

def get_all_sessions():
    """Return all sessions ordered by most recent."""
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT * FROM sessions ORDER BY last_updated DESC"
        ).fetchall()
        return [dict(row) for row in rows]

def get_messages(session_id: int):
    """Return all messages for a given session."""
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT role, content FROM messages WHERE session_id = ? ORDER BY id ASC",
            (session_id,)
        ).fetchall()
        return [{"role": row["role"], "content": row["content"]} for row in rows]

def delete_session(session_id: int):
    """Delete a session and all its messages."""
    with get_connection() as conn:
        conn.execute("DELETE FROM messages WHERE session_id = ?", (session_id,))
        conn.execute("DELETE FROM sessions WHERE id = ?", (session_id,))
        conn.commit()

def update_session_title(session_id: int, title: str):
    """Update the title of a session."""
    with get_connection() as conn:
        conn.execute(
            "UPDATE sessions SET title = ? WHERE id = ?",
            (title, session_id)
        )
        conn.commit()
