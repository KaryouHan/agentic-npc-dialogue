import json
import os
import sqlite3
from pathlib import Path
from typing import Any

from npc_state import INITIAL_NPC_STATE

BASE_DIR = Path(__file__).resolve().parent


def _db_path() -> Path:
    database_url = os.getenv("DATABASE_URL", "sqlite:///./npc_memory.db")
    if database_url.startswith("sqlite:///"):
        path = Path(database_url.replace("sqlite:///", "", 1))
        if not path.is_absolute():
            return BASE_DIR / path
        return path
    return BASE_DIR / "npc_memory.db"


DB_PATH = _db_path()


def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    with get_connection() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS npc_state (
                id INTEGER PRIMARY KEY CHECK (id = 1),
                state_json TEXT NOT NULL
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS dialogue_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                role TEXT NOT NULL,
                content TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS memories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                content TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        row = conn.execute("SELECT id FROM npc_state WHERE id = 1").fetchone()
        if row is None:
            save_npc_state(INITIAL_NPC_STATE, conn)


def load_npc_state() -> dict[str, Any]:
    with get_connection() as conn:
        row = conn.execute("SELECT state_json FROM npc_state WHERE id = 1").fetchone()
    if row is None:
        return dict(INITIAL_NPC_STATE)
    return json.loads(row["state_json"])


def save_npc_state(state: dict[str, Any], conn: sqlite3.Connection | None = None) -> None:
    payload = json.dumps(state, ensure_ascii=False)
    if conn is not None:
        conn.execute(
            "INSERT OR REPLACE INTO npc_state (id, state_json) VALUES (1, ?)",
            (payload,),
        )
        return
    with get_connection() as owned_conn:
        owned_conn.execute(
            "INSERT OR REPLACE INTO npc_state (id, state_json) VALUES (1, ?)",
            (payload,),
        )


def add_history(role: str, content: str) -> None:
    with get_connection() as conn:
        conn.execute(
            "INSERT INTO dialogue_history (role, content) VALUES (?, ?)",
            (role, content),
        )


def get_recent_history(limit: int = 12) -> list[dict[str, str]]:
    with get_connection() as conn:
        rows = conn.execute(
            """
            SELECT role, content
            FROM dialogue_history
            ORDER BY id DESC
            LIMIT ?
            """,
            (limit,),
        ).fetchall()
    return [{"role": row["role"], "content": row["content"]} for row in reversed(rows)]


def add_memory(content: str) -> None:
    if not content.strip():
        return
    with get_connection() as conn:
        conn.execute("INSERT INTO memories (content) VALUES (?)", (content.strip(),))


def get_recent_memories(limit: int = 8) -> list[str]:
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT content FROM memories ORDER BY id DESC LIMIT ?",
            (limit,),
        ).fetchall()
    return [row["content"] for row in reversed(rows)]


def reset_demo() -> None:
    with get_connection() as conn:
        conn.execute("DELETE FROM dialogue_history")
        conn.execute("DELETE FROM memories")
        save_npc_state(dict(INITIAL_NPC_STATE), conn)
