"""
Theme constants matching the React T object for visual parity.
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

# ── Plotly Layout Template ────────────────────────────────────
def plotly_layout(**kwargs):
    """Return a consistent Plotly layout dict."""
    base = dict(
        font=dict(family="DM Sans, -apple-system, sans-serif", color=TEXT),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=40, r=20, t=30, b=40),
        xaxis=dict(gridcolor=GRID, gridwidth=1),
        yaxis=dict(gridcolor=GRID, gridwidth=1),
        legend=dict(font=dict(size=11)),
        hoverlabel=dict(
            bgcolor=SURFACE,
            bordercolor=BORDER,
            font=dict(family="DM Sans, sans-serif", size=12),
        ),
    )
    base.update(kwargs)
    return base


# ── Custom CSS for Streamlit ──────────────────────────────────
CUSTOM_CSS = """
<style>
    /* KPI Metric styling */
    div[data-testid="stMetric"] {
        background: white;
        border: 1px solid #e2e5ea;
        border-radius: 10px;
        padding: 12px 16px;
    }
    div[data-testid="stMetric"] label {
        font-size: 11px !important;
        font-weight: 600 !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    div[data-testid="stMetric"] [data-testid="stMetricValue"] {
        font-family: 'JetBrains Mono', monospace;
        font-size: 26px !important;
    }

    /* Form container */
    div[data-testid="stForm"] {
        border: 1px solid #e2e5ea !important;
        border-radius: 10px !important;
        padding: 16px !important;
    }

    /* Footer */
    footer {visibility: hidden;}

    /* Main block */
    .block-container {
        padding-top: 1.5rem !important;
        max-width: 1200px;
    }
</style>
"""
