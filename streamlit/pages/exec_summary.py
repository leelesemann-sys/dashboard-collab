"""Executive Summary — KPIs + TRx Line + Revenue Bar."""
import streamlit as st
import plotly.graph_objects as go

from lib.mock_data import df_monthly, kpis, short_month
from lib.theme import ACCENT1, TEXT_DIM, GREEN, RED, plotly_layout, render_kpis
from lib.feedback_ui import section_with_feedback, close_section, element_feedback, feedback_section


def show():
    st.markdown("## 📊 Executive Summary")

    # ── KPIs (HTML cards) ─────────────────────────────────────
    rev_delta = (kpis["cumulative_net_revenue"] / 600_000 - 1) * 100
    trx_delta = (kpis["cumulative_trx"] / 8500 - 1) * 100
    doc_delta = (kpis["active_prescribers"] / 70 - 1) * 100
    ms_delta = kpis["market_share_latest"] - 25

    render_kpis(st.columns(4), [
        {"label": "Net Revenue kum.", "value": f"€{kpis['cumulative_net_revenue']:,.0f}",
         "sub": "Ziel: €600.000", "trend": f"{rev_delta:+.1f}%",
         "trend_color": GREEN if rev_delta >= 0 else RED},
        {"label": "TRx kumuliert", "value": f"{kpis['cumulative_trx']:,}",
         "sub": "Ziel: 8.500", "trend": f"{trx_delta:+.1f}%",
         "trend_color": GREEN if trx_delta >= 0 else RED},
        {"label": "Aktive Verordner", "value": str(kpis["active_prescribers"]),
         "sub": "Ziel: 70", "trend": f"{doc_delta:+.1f}%",
         "trend_color": GREEN if doc_delta >= 0 else RED},
        {"label": "Marktanteil", "value": f"{kpis['market_share_latest']}%",
         "sub": "Ziel: 25%", "trend": f"{ms_delta:+.1f}pp",
         "trend_color": GREEN if ms_delta >= 0 else RED},
    ])

    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

    # ── Charts ────────────────────────────────────────────────
    df = df_monthly.copy()
    df["month_label"] = df["month"].apply(short_month)

    col1, col2 = st.columns(2)

    with col1:
        section_with_feedback("exec-summary", "trx-chart", "TRx Entwicklung", "Ist vs. Plan — monatliche Verordnungen")

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=df["month_label"], y=df["trx"], mode="lines+markers",
            name="Ist", line=dict(color=ACCENT1, width=2.5),
            marker=dict(size=7, color=ACCENT1),
        ))
        fig.add_trace(go.Scatter(
            x=df["month_label"], y=df["trx_plan"], mode="lines",
            name="Plan", line=dict(color=TEXT_DIM, width=1.5, dash="dash"),
        ))
        fig.update_layout(**plotly_layout(height=280))
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        close_section()

    with col2:
        section_with_feedback("exec-summary", "revenue-chart", "Net Revenue", "Monatlich Ist vs. Plan (€)")

        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=df["month_label"], y=df["net_revenue"], name="Ist",
            marker_color=ACCENT1, marker_cornerradius=4,
        ))
        fig.add_trace(go.Bar(
            x=df["month_label"], y=df["net_plan"], name="Plan",
            marker_color=TEXT_DIM, opacity=0.3, marker_cornerradius=4,
        ))
        fig.update_layout(**plotly_layout(height=280, barmode="group"))
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        close_section()

    # ── Feedback ──────────────────────────────────────────────
    feedback_section("exec-summary")
