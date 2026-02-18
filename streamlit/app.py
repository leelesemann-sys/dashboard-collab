"""
Dashboard Prototyper — Streamlit Variant
=========================================
Iterative dashboard prototyping with built-in feedback collection.
Uses st.navigation() + st.Page() API for multi-page routing.
"""
import streamlit as st

st.set_page_config(
    page_title="Dashboard Prototyper — Streamlit",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ────────────────────────────────────────────────
from lib.theme import CUSTOM_CSS
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# ── Page imports ──────────────────────────────────────────────
from pages.exec_summary import show as exec_show
from pages.market_uptake import show as uptake_show
from pages.regional_view import show as regional_show
from pages.feedback_overview import show as feedback_show

# ── Sidebar: Round selector ──────────────────────────────────
from lib import feedback_db

with st.sidebar:
    st.title("📋 Dashboard Prototyper")
    st.caption("Streamlit-Variante")
    st.markdown("---")

    max_round = feedback_db.get_max_round()
    round_options = list(range(1, max_round + 2))  # +1 for "next round"

    current_round = st.selectbox(
        "🔄 Aktuelle Runde",
        options=round_options,
        index=0,
        format_func=lambda x: f"Runde {x}" + (" (neu)" if x > max_round else ""),
    )
    st.session_state["current_round"] = current_round

    st.markdown("---")
    st.caption("Feedback wird in SQLite gespeichert und ist für alle Nutzer sichtbar.")

# ── Page Navigation ───────────────────────────────────────────
exec_page = st.Page(exec_show, title="Executive Summary", icon="📊", url_path="exec", default=True)
uptake_page = st.Page(uptake_show, title="Markt-Uptake", icon="📈", url_path="uptake")
regional_page = st.Page(regional_show, title="Regionale Performance", icon="🗺", url_path="regional")
feedback_page = st.Page(feedback_show, title="Feedback-Übersicht", icon="💬", url_path="feedback")

nav = st.navigation(
    {
        "Dashboard": [exec_page, uptake_page, regional_page],
        "Admin": [feedback_page],
    }
)
nav.run()
