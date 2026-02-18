"""
SQLite-based feedback persistence for the Streamlit variant.
Auto-creates feedback.db on first run.
"""
import sqlite3
from datetime import datetime
from pathlib import Path
import pandas as pd

DB_PATH = Path(__file__).parent.parent / "data" / "feedback.db"


def _conn():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    return sqlite3.connect(str(DB_PATH))


def init_db():
    """Create feedback table if it doesn't exist."""
    with _conn() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS feedback (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                page_id     TEXT NOT NULL,
                round       INTEGER NOT NULL,
                author      TEXT NOT NULL,
                comment     TEXT NOT NULL,
                rating      INTEGER NOT NULL CHECK(rating BETWEEN 1 AND 5),
                status      TEXT NOT NULL DEFAULT 'open' CHECK(status IN ('open','resolved')),
                created_at  TEXT NOT NULL
            )
        """)


def add_feedback(page_id: str, round_num: int, author: str, comment: str, rating: int):
    """Insert a new feedback entry."""
    with _conn() as conn:
        conn.execute(
            "INSERT INTO feedback (page_id, round, author, comment, rating, status, created_at) VALUES (?,?,?,?,?,?,?)",
            (page_id, round_num, author, comment, rating, "open", datetime.now().isoformat()),
        )


def get_feedback(page_id: str = None, round_num: int = None, status: str = None) -> pd.DataFrame:
    """Retrieve feedback with optional filters, returns DataFrame."""
    query = "SELECT * FROM feedback WHERE 1=1"
    params = []
    if page_id:
        query += " AND page_id = ?"
        params.append(page_id)
    if round_num:
        query += " AND round = ?"
        params.append(round_num)
    if status:
        query += " AND status = ?"
        params.append(status)
    query += " ORDER BY created_at DESC"

    with _conn() as conn:
        return pd.read_sql_query(query, conn, params=params)


def update_status(feedback_id: int, new_status: str):
    """Toggle feedback status (open/resolved)."""
    with _conn() as conn:
        conn.execute("UPDATE feedback SET status = ? WHERE id = ?", (new_status, feedback_id))


def get_max_round() -> int:
    """Return the highest round number in the database."""
    with _conn() as conn:
        result = conn.execute("SELECT MAX(round) FROM feedback").fetchone()
        return result[0] if result[0] else 1


def export_dataframe() -> pd.DataFrame:
    """Return all feedback as a DataFrame for export."""
    with _conn() as conn:
        return pd.read_sql_query("SELECT * FROM feedback ORDER BY round, page_id, created_at", conn)


# Initialize on import
init_db()
