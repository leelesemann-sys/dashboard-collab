"""
Dashboard Prototyper — Streamlit Variant
=========================================
Iterative dashboard prototyping with built-in feedback collection.
Premium styling with HTML KPI cards and custom CSS.
"""
import streamlit as st

st.set_page_config(
    page_title="Dashboard Prototyper — Streamlit",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Reload all modules to bust .pyc cache on Streamlit Cloud ────
import importlib
import lib.mock_data, lib.theme, lib.feedback_db, lib.feedback_ui
importlib.reload(lib.mock_data)
importlib.reload(lib.theme)
importlib.reload(lib.feedback_db)
importlib.reload(lib.feedback_ui)

import pages.exec_summary, pages.market_uptake, pages.regional_view, pages.feedback_overview
importlib.reload(pages.exec_summary)
importlib.reload(pages.market_uptake)
importlib.reload(pages.regional_view)
importlib.reload(pages.feedback_overview)

from lib.theme import CUSTOM_CSS
from pages.exec_summary import show as exec_show
from pages.market_uptake import show as uptake_show
from pages.regional_view import show as regional_show
from pages.feedback_overview import show as feedback_show

# ── Custom CSS (after reload) ───────────────────────────────────
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# ── Sidebar ───────────────────────────────────────────────────
from lib import feedback_db

with st.sidebar:
    st.markdown("""
    <div style="margin-bottom:8px">
        <div style="font-size:18px; font-weight:700; color:#1a202c; font-family:'DM Sans',sans-serif;">
            📋 Dashboard Prototyper
        </div>
        <div style="font-size:12px; color:#6b7280; font-family:'JetBrains Mono',mono; margin-top:2px;">
            Streamlit-Variante
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    max_round = feedback_db.get_max_round()
    round_options = list(range(1, max_round + 2))

    current_round = st.selectbox(
        "🔄 Aktuelle Runde",
        options=round_options,
        index=0,
        format_func=lambda x: f"Runde {x}" + (" ← neu" if x > max_round else f" ({len(feedback_db.get_feedback(round_num=x))} Kommentare)"),
    )
    st.session_state["current_round"] = current_round

    st.markdown("---")

    # Sidebar stats
    df_all = feedback_db.export_dataframe()
    if not df_all.empty:
        open_count = len(df_all[df_all["status"] == "open"])
        resolved_count = len(df_all[df_all["status"] == "resolved"])
        st.markdown(f"""
        <div style="background:#ffffff; border:1px solid #e2e5ea; border-radius:8px; padding:12px; font-size:12px;">
            <div style="font-weight:600; color:#1a202c; margin-bottom:6px;">📊 Status</div>
            <div style="display:flex; justify-content:space-between; margin-bottom:4px;">
                <span style="color:#6b7280">Gesamt:</span>
                <span style="font-weight:600; font-family:'JetBrains Mono',mono">{len(df_all)}</span>
            </div>
            <div style="display:flex; justify-content:space-between; margin-bottom:4px;">
                <span style="color:#6b7280">🔲 Offen:</span>
                <span style="font-weight:600; font-family:'JetBrains Mono',mono; color:#d97706">{open_count}</span>
            </div>
            <div style="display:flex; justify-content:space-between;">
                <span style="color:#6b7280">✅ Erledigt:</span>
                <span style="font-weight:600; font-family:'JetBrains Mono',mono; color:#059669">{resolved_count}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="font-size:12px; color:#9ca3af; text-align:center; padding:12px;">
            Noch kein Feedback abgegeben.
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
    st.caption("Feedback in Google Sheet · Sichtbar für alle Nutzer")

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
