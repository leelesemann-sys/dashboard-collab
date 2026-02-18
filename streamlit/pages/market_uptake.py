"""Market Uptake — NRx/RRx + Competitor Market Shares."""
import streamlit as st
import plotly.graph_objects as go

from lib.mock_data import df_monthly, df_competitors, short_month
from lib.theme import ACCENT1, ACCENT2, FORXIGA, JARDIANCE, INVOKANA, TEXT_DIM, plotly_layout, render_kpis
from lib.feedback_ui import section_with_feedback, feedback_section


def show():
    st.markdown("## 📈 Markt-Uptake & Verordner")

    df = df_monthly.copy()
    cum_nrx = int(df["nrx"].sum())
    cum_rrx = int(df["rrx"].sum())
    repeat_ratio = (cum_rrx / (cum_nrx + cum_rrx) * 100) if (cum_nrx + cum_rrx) > 0 else 0
    last = df.iloc[-1]

    # ── KPIs ──────────────────────────────────────────────────
    render_kpis(st.columns(4), [
        {"label": "NRx kumuliert", "value": f"{cum_nrx:,}", "sub": "kumuliert Mai–Dez"},
        {"label": "RRx kumuliert", "value": f"{cum_rrx:,}", "sub": "kumuliert Mai–Dez"},
        {"label": "Repeat-Rate", "value": f"{repeat_ratio:.1f}%", "sub": "RRx / (NRx+RRx)"},
        {"label": "Verordner aktuell", "value": str(int(last["prescribers"])), "sub": "aktueller Monat"},
    ])

    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

    # ── Charts ────────────────────────────────────────────────
    df["month_label"] = df["month"].apply(short_month)
    col1, col2 = st.columns(2)

    with col1:
        section_with_feedback("market-uptake", "nrx-rrx-chart", "NRx vs. RRx", "Neue vs. wiederholte Verordnungen")

        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=df["month_label"], y=df["nrx"], name="NRx",
            marker_color=ACCENT1,
        ))
        fig.add_trace(go.Bar(
            x=df["month_label"], y=df["rrx"], name="RRx",
            marker_color=ACCENT2, marker_cornerradius=4,
        ))
        fig.update_layout(**plotly_layout(height=280, barmode="stack"))
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    with col2:
        section_with_feedback("market-uptake", "market-share-chart", "Marktanteile SGLT2i", "Monatliche Entwicklung (%)")

        dfc = df_competitors.copy()
        dfc["month_label"] = dfc["month"].apply(short_month)
        fig = go.Figure()
        for col_name, color, label in [
            ("cardiozan", ACCENT1, "Cardiozan"),
            ("forxiga", FORXIGA, "Forxiga"),
            ("jardiance", JARDIANCE, "Jardiance"),
            ("invokana", INVOKANA, "Invokana"),
        ]:
            fig.add_trace(go.Scatter(
                x=dfc["month_label"], y=dfc[col_name], name=label,
                mode="lines", stackgroup="one",
                line=dict(width=0.5, color=color),
                fillcolor=color,
            ))
        fig.update_layout(**plotly_layout(
            height=280, yaxis=dict(range=[0, 100], gridcolor="#e5e7eb"),
        ))
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    # ── Feedback ──────────────────────────────────────────────
    feedback_section("market-uptake")
