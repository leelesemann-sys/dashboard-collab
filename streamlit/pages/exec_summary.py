"""Executive Summary — KPIs + TRx Line + Revenue Bar."""
import streamlit as st
import plotly.graph_objects as go

from lib.mock_data import df_monthly, kpis, short_month
from lib.theme import ACCENT1, TEXT_DIM, GRID, plotly_layout
from lib import feedback_db


def show():
    st.header("📊 Executive Summary")

    # ── KPIs ──────────────────────────────────────────────────
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Net Revenue kum.", f"€{kpis['cumulative_net_revenue']:,.0f}", delta=f"{(kpis['cumulative_net_revenue']/600000-1)*100:+.1f}%")
    c2.metric("TRx kumuliert", f"{kpis['cumulative_trx']:,}", delta=f"{(kpis['cumulative_trx']/8500-1)*100:+.1f}%")
    c3.metric("Aktive Verordner", kpis["active_prescribers"], delta=f"{(kpis['active_prescribers']/70-1)*100:+.1f}%")
    c4.metric("Marktanteil", f"{kpis['market_share_latest']}%", delta=f"{kpis['market_share_latest']-25:+.1f}pp")

    st.markdown("---")

    # ── Charts ────────────────────────────────────────────────
    col1, col2 = st.columns(2)

    df = df_monthly.copy()
    df["month_label"] = df["month"].apply(short_month)

    with col1:
        st.subheader("TRx Entwicklung")
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=df["month_label"], y=df["trx"], mode="lines+markers",
            name="Ist", line=dict(color=ACCENT1, width=2.5), marker=dict(size=6),
        ))
        fig.add_trace(go.Scatter(
            x=df["month_label"], y=df["trx_plan"], mode="lines",
            name="Plan", line=dict(color=TEXT_DIM, width=1.5, dash="dash"),
        ))
        fig.update_layout(**plotly_layout(height=300, xaxis_title=None, yaxis_title="TRx"))
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Net Revenue")
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=df["month_label"], y=df["net_revenue"], name="Ist",
            marker_color=ACCENT1, marker_cornerradius=4,
        ))
        fig.add_trace(go.Bar(
            x=df["month_label"], y=df["net_plan"], name="Plan",
            marker_color=TEXT_DIM, opacity=0.3, marker_cornerradius=4,
        ))
        fig.update_layout(**plotly_layout(height=300, barmode="group", xaxis_title=None, yaxis_title="€"))
        st.plotly_chart(fig, use_container_width=True)

    # ── Feedback ──────────────────────────────────────────────
    _feedback_section("exec-summary")


def _feedback_section(page_id: str):
    """Reusable feedback form + history block."""
    current_round = st.session_state.get("current_round", 1)

    st.markdown("---")
    st.subheader("💬 Feedback zu dieser Seite")

    with st.form(f"feedback_{page_id}_r{current_round}", clear_on_submit=True):
        fc1, fc2 = st.columns([3, 1])
        author = fc1.text_input("Dein Name")
        rating = fc2.slider("Bewertung", 1, 5, 3)
        comment = st.text_area("Kommentar")
        submitted = st.form_submit_button("📩 Absenden")
        if submitted and author.strip() and comment.strip():
            feedback_db.add_feedback(page_id, current_round, author.strip(), comment.strip(), rating)
            st.rerun()

    # History
    df_fb = feedback_db.get_feedback(page_id=page_id)
    if not df_fb.empty:
        st.caption(f"Bisheriges Feedback ({len(df_fb)})")
        for _, row in df_fb.iterrows():
            stars = "★" * int(row["rating"]) + "☆" * (5 - int(row["rating"]))
            status_icon = "✅" if row["status"] == "resolved" else "🔲"
            with st.container(border=True):
                hc1, hc2, hc3, hc4 = st.columns([2, 4, 1, 1])
                hc1.markdown(f"**{row['author']}**  \n`Runde {row['round']}`")
                hc2.write(row["comment"])
                hc3.write(stars)
                if hc4.button(status_icon, key=f"toggle_{row['id']}"):
                    new_status = "resolved" if row["status"] == "open" else "open"
                    feedback_db.update_status(int(row["id"]), new_status)
                    st.rerun()
