"""
Google Sheets-based feedback persistence for the Streamlit variant.
Replaces the previous SQLite backend. Same API surface — all callers
(feedback_ui.py, pages/, app.py) remain unchanged.

Requires:
  - gspread + google-auth
  - st.secrets["gcp_service_account"] with service account JSON
  - st.secrets["google_sheets"]["spreadsheet_url"]
"""
import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
import pandas as pd

# ── Column order in the Sheet (must match header row) ────────
COLUMNS = ["id", "page_id", "element_id", "round", "author",
           "comment", "rating", "status", "created_at", "source"]

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]


@st.cache_resource(show_spinner=False)
def _get_client():
    """Authenticate once and cache the gspread client."""
    creds = Credentials.from_service_account_info(
        st.secrets["gcp_service_account"], scopes=SCOPES,
    )
    return gspread.authorize(creds)


def _sheet():
    """Return the 'feedback' worksheet (tab)."""
    client = _get_client()
    url = st.secrets["google_sheets"]["spreadsheet_url"]
    spreadsheet = client.open_by_url(url)
    return spreadsheet.worksheet("feedback")


def _next_id() -> str:
    """Generate a short unique ID (matching React's nextId pattern)."""
    import time, random, string
    t = int(time.time() * 1000)
    base36 = ""
    while t > 0:
        base36 = string.digits + string.ascii_lowercase[: 26][t % 36] if False else ""
        break
    # Simple approach: timestamp hex + random suffix
    return f"{int(time.time()):x}{random.randint(1000, 9999)}"


def _load_all() -> pd.DataFrame:
    """Load all rows from the sheet into a DataFrame.

    Uses session_state cache to avoid repeated API calls within a single
    Streamlit rerun. Cache is invalidated on write operations.
    """
    if "_feedback_cache" not in st.session_state:
        ws = _sheet()
        records = ws.get_all_records(expected_headers=COLUMNS)
        df = pd.DataFrame(records)
        if df.empty:
            df = pd.DataFrame(columns=COLUMNS)
        else:
            # Type coercion
            df["round"] = pd.to_numeric(df["round"], errors="coerce").fillna(1).astype(int)
            df["rating"] = pd.to_numeric(df["rating"], errors="coerce").fillna(3).astype(int)
            df["id"] = df["id"].astype(str)
            # Treat empty strings as None for element_id
            df["element_id"] = df["element_id"].replace("", None)
        st.session_state["_feedback_cache"] = df
    return st.session_state["_feedback_cache"]


def _invalidate_cache():
    """Clear cached data so next read fetches fresh from the sheet."""
    st.session_state.pop("_feedback_cache", None)


# ── Public API (same signatures as the old SQLite version) ───


def add_feedback(page_id: str, round_num: int, author: str, comment: str,
                 rating: int, element_id: str = None):
    """Insert a new feedback entry into the Google Sheet."""
    row_id = _next_id()
    row = [
        row_id,
        page_id,
        element_id or "",
        round_num,
        author,
        comment,
        rating,
        "open",
        datetime.now().isoformat(),
        "streamlit",
    ]
    ws = _sheet()
    ws.append_row(row, value_input_option="USER_ENTERED")
    _invalidate_cache()


def get_feedback(page_id: str = None, round_num: int = None,
                 status: str = None, element_id: str = "__unset__") -> pd.DataFrame:
    """Retrieve feedback with optional filters, returns DataFrame."""
    df = _load_all().copy()
    if df.empty:
        return df

    if page_id:
        df = df[df["page_id"] == page_id]
    if element_id != "__unset__":
        if element_id is None:
            df = df[df["element_id"].isna()]
        else:
            df = df[df["element_id"] == element_id]
    if round_num:
        df = df[df["round"] == round_num]
    if status:
        df = df[df["status"] == status]

    return df.sort_values("created_at", ascending=False).reset_index(drop=True)


def get_element_count(page_id: str, element_id: str) -> int:
    """Count feedback entries for a specific element."""
    df = _load_all()
    if df.empty:
        return 0
    return len(df[(df["page_id"] == page_id) & (df["element_id"] == element_id)])


def update_status(feedback_id: int, new_status: str):
    """Toggle feedback status (open/resolved) in the Sheet."""
    feedback_id = str(feedback_id)
    ws = _sheet()
    # Find the row by scanning column A (id)
    id_cells = ws.col_values(1)  # column A = id
    for i, cell_val in enumerate(id_cells):
        if str(cell_val) == feedback_id:
            ws.update_cell(i + 1, 8, new_status)  # column H = status
            _invalidate_cache()
            return
    # If not found, silently return (may be stale data)


def get_max_round() -> int:
    """Return the highest round number in the Sheet."""
    df = _load_all()
    if df.empty:
        return 1
    max_r = df["round"].max()
    return int(max_r) if pd.notna(max_r) else 1


def export_dataframe() -> pd.DataFrame:
    """Return all feedback as a DataFrame for export."""
    df = _load_all().copy()
    if df.empty:
        return df
    return df.sort_values(["round", "page_id", "created_at"]).reset_index(drop=True)
