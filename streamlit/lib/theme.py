"""
Theme constants matching the React T object for visual parity.
Includes HTML KPI cards and premium CSS styling.
"""

# ── Colors ────────────────────────────────────────────────────
BG = "#f5f6f8"
SURFACE = "#ffffff"
SURFACE2 = "#f0f2f5"
BORDER = "#e2e5ea"
TEXT = "#1a202c"
TEXT_MUTED = "#6b7280"
TEXT_DIM = "#9ca3af"
ACCENT1 = "#2563eb"
ACCENT2 = "#0891b2"
GREEN = "#059669"
RED = "#dc2626"
YELLOW = "#d97706"
GRID = "#e5e7eb"

# Competitor colors
FORXIGA = "#64748b"
JARDIANCE = "#78716c"
INVOKANA = "#94a3b8"


# ── HTML KPI Card ─────────────────────────────────────────────

def kpi_card(label: str, value: str, sub: str = "", trend: str = "", trend_color: str = "") -> str:
    """Return styled HTML for a KPI card matching the React variant."""
    trend_html = ""
    if trend:
        tc = trend_color or TEXT_MUTED
        trend_html = f'<div class="kpi-trend" style="color:{tc}">{trend}</div>'
    sub_html = f'<div class="kpi-sub">{sub}</div>' if sub else ""
    return (
        f'<div class="kpi-card">'
        f'<div class="kpi-label">{label}</div>'
        f'<div class="kpi-value">{value}</div>'
        f'{sub_html}'
        f'{trend_html}'
        f'</div>'
    )


def render_kpis(cols, kpis_data):
    """Render a row of KPI cards into Streamlit columns.

    kpis_data: list of dicts with keys: label, value, sub, trend, trend_color
    """
    import streamlit as st
    for col, kpi in zip(cols, kpis_data):
        col.markdown(
            kpi_card(
                label=kpi.get("label", ""),
                value=kpi.get("value", ""),
                sub=kpi.get("sub", ""),
                trend=kpi.get("trend", ""),
                trend_color=kpi.get("trend_color", ""),
            ),
            unsafe_allow_html=True,
        )


# ── Section Card (HTML container) ────────────────────────────

def section_card(title: str, subtitle: str = "") -> str:
    """Return opening HTML for a styled section card. Close with </div>."""
    sub_html = f'<div class="section-sub">{subtitle}</div>' if subtitle else ""
    return f"""<div class="section-card">
        <div class="section-title">{title}</div>
        {sub_html}
    """


# ── Plotly Layout Template ────────────────────────────────────

def plotly_layout(**kwargs):
    """Return a consistent Plotly layout dict with premium styling."""
    base = dict(
        font=dict(family="DM Sans, -apple-system, sans-serif", color=TEXT, size=12),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=50, r=20, t=36, b=44),
        xaxis=dict(
            gridcolor=GRID, gridwidth=1,
            tickfont=dict(size=11, color=TEXT_MUTED),
            title_font=dict(size=12, color=TEXT_MUTED),
        ),
        yaxis=dict(
            gridcolor=GRID, gridwidth=1,
            tickfont=dict(size=11, color=TEXT_MUTED),
            title_font=dict(size=12, color=TEXT_MUTED),
        ),
        legend=dict(
            font=dict(size=11),
            bgcolor="rgba(255,255,255,0.8)",
            bordercolor=BORDER,
            borderwidth=1,
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="left",
            x=0,
        ),
        hoverlabel=dict(
            bgcolor=SURFACE,
            bordercolor=BORDER,
            font=dict(family="DM Sans, sans-serif", size=12, color=TEXT),
        ),
        hovermode="x unified",
    )
    base.update(kwargs)
    return base


# ── Custom CSS for Streamlit ──────────────────────────────────

CUSTOM_CSS = """
<link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=JetBrains+Mono:wght@400;600;700&display=swap" rel="stylesheet">
<style>
    /* ── Global ──────────────────────────────────────── */
    .block-container {
        padding-top: 2.5rem !important;
        padding-bottom: 0.5rem !important;
        max-width: 1200px;
    }
    html, body, [class*="css"] {
        font-family: 'DM Sans', -apple-system, sans-serif !important;
    }
    footer { visibility: hidden; }
    header[data-testid="stHeader"] {
        background: rgba(255,255,255,0.95) !important;
        backdrop-filter: blur(8px);
        border-bottom: 1px solid #e2e5ea;
    }

    /* ── Sidebar ─────────────────────────────────────── */
    div[data-testid="stSidebar"] {
        background: #f8fafc !important;
        border-right: 1px solid #e2e5ea;
    }
    div[data-testid="stSidebar"] > div:first-child {
        padding-top: 1.5rem;
    }

    /* ── KPI Cards (HTML) ────────────────────────────── */
    .kpi-card {
        background: #ffffff;
        border: 1.5px solid #e2e5ea;
        border-radius: 10px;
        padding: 14px 16px;
        text-align: left;
        box-shadow: 0 1px 3px rgba(0,0,0,0.04);
        transition: box-shadow 0.15s, border-color 0.15s;
    }
    .kpi-card:hover {
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        border-color: #d0d5dd;
    }
    .kpi-label {
        font-size: 11px;
        font-weight: 600;
        color: #6b7280;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        font-family: 'DM Sans', sans-serif;
    }
    .kpi-value {
        font-size: 26px;
        font-weight: 700;
        color: #1a202c;
        font-family: 'JetBrains Mono', monospace;
        margin-top: 4px;
        line-height: 1.2;
    }
    .kpi-sub {
        font-size: 12px;
        color: #6b7280;
        font-family: 'JetBrains Mono', monospace;
        margin-top: 2px;
    }
    .kpi-trend {
        font-size: 13px;
        font-weight: 600;
        font-family: 'JetBrains Mono', monospace;
        margin-top: 4px;
    }

    /* ── Section Cards ───────────────────────────────── */
    .section-card {
        background: #ffffff;
        border: 1px solid #e2e5ea;
        border-radius: 10px;
        padding: 18px 20px;
        margin-bottom: 14px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.04);
    }
    .section-title {
        font-weight: 600;
        font-size: 14px;
        color: #1a202c;
        margin-bottom: 4px;
    }
    .section-sub {
        font-size: 12px;
        color: #6b7280;
        margin-bottom: 12px;
    }

    /* ── Feedback History Items ───────────────────────── */
    .feedback-item {
        display: flex;
        align-items: flex-start;
        gap: 12px;
        padding: 10px 14px;
        background: #f0f2f5;
        border-radius: 8px;
        border: 1px solid #e2e5ea;
        margin-bottom: 8px;
    }
    .feedback-item.resolved {
        background: rgba(5,150,105,0.04);
        border-color: rgba(5,150,105,0.15);
    }
    .feedback-author {
        font-weight: 600;
        font-size: 13px;
        color: #1a202c;
    }
    .feedback-round {
        font-size: 11px;
        color: #6b7280;
        font-family: 'JetBrains Mono', monospace;
    }
    .feedback-stars {
        font-size: 12px;
        color: #d97706;
    }
    .feedback-comment {
        font-size: 13px;
        color: #1a202c;
        line-height: 1.5;
    }
    .feedback-time {
        font-size: 11px;
        color: #9ca3af;
        font-family: 'JetBrains Mono', monospace;
        margin-top: 4px;
    }

    /* ── Override st.metric (fallback) ───────────────── */
    div[data-testid="stMetric"] {
        background: white;
        border: 1.5px solid #e2e5ea;
        border-radius: 10px;
        padding: 12px 16px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.04);
    }
    div[data-testid="stMetric"] label {
        font-size: 11px !important;
        font-weight: 600 !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    div[data-testid="stMetric"] [data-testid="stMetricValue"] {
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 24px !important;
    }

    /* ── Form styling ────────────────────────────────── */
    div[data-testid="stForm"] {
        border: 1px solid #e2e5ea !important;
        border-radius: 10px !important;
        padding: 16px !important;
        background: #ffffff !important;
        box-shadow: 0 1px 3px rgba(0,0,0,0.04);
    }

    /* ── Tabs styling ────────────────────────────────── */
    button[data-baseweb="tab"] {
        font-family: 'DM Sans', sans-serif !important;
        font-weight: 500 !important;
        font-size: 13px !important;
    }

    /* ── Page title styling ───────────────────────────── */
    h1 {
        font-family: 'DM Sans', sans-serif !important;
        font-weight: 700 !important;
        font-size: 22px !important;
        color: #1a202c !important;
    }
    h2, h3 {
        font-family: 'DM Sans', sans-serif !important;
        font-weight: 600 !important;
    }

    /* ── Dataframe styling ───────────────────────────── */
    div[data-testid="stDataFrame"] {
        border: 1px solid #e2e5ea;
        border-radius: 10px;
        overflow: hidden;
    }

    /* ── Download buttons ────────────────────────────── */
    div[data-testid="stDownloadButton"] > button {
        border: 1px solid #e2e5ea !important;
        border-radius: 6px !important;
        font-family: 'DM Sans', sans-serif !important;
        font-weight: 600 !important;
        font-size: 12px !important;
        box-shadow: 0 1px 2px rgba(0,0,0,0.04) !important;
    }
</style>
"""
