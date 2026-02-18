"""Market Uptake — NRx/RRx + Competitor Market Shares."""
import streamlit as st
import plotly.graph_objects as go

from lib.mock_data import df_monthly, df_competitors, short_month
from lib.theme import ACCENT1, ACCENT2, FORXIGA, JARDIANCE, INVOKANA, TEXT_DIM, plotly_layout
from lib import feedback_db


def show():
    st.header("📈 Markt-Uptake & Verordner")

    df = df_monthly.copy()
    cum_nrx = df["nrx"].sum()
    cum_rrx = df["rrx"].sum()
    repeat_ratio = (cum_rrx / (cum_nrx + cum_rrx) * 100) if (cum_nrx + cum_rrx) > 0 else 0
    last = df.iloc[-1]

    # ── KPIs ──────────────────────────────────────────────────
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("NRx kumuliert", f"{cum_nrx:,}")
    c2.metric("RRx kumuliert", f"{cum_rrx:,}")
    c3.metric("Repeat-Rate", f"{repeat_ratio:.1f}%")
    c4.metric("Verordner aktuell", int(last["prescribers"]))

    st.markdown("---")

    # ── Charts ────────────────────────────────────────────────
    col1, col2 = st.columns(2)

    df["month_label"] = df["month"].apply(short_month)

    with col1:
        st.subheader("NRx vs. RRx")
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=df["month_label"], y=df["nrx"], name="NRx",
            marker_color=ACCENT1, marker_cornerradius=0,
        ))
        fig.add_trace(go.Bar(
            x=df["month_label"], y=df["rrx"], name="RRx",
            marker_color=ACCENT2, marker_cornerradius=4,
        ))
        fig.update_layout(**plotly_layout(
            height=300, barmode="stack", xaxis_title=None, yaxis_title="Verordnungen",
        ))
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Marktanteile SGLT2i")
        dfc = df_competitors.copy()
        dfc["month_label"] = dfc["month"].apply(short_month)
        fig = go.Figure()
        for col_name, color in [("cardiozan", ACCENT1), ("forxiga", FORXIGA), ("jardiance", JARDIANCE), ("invokana", INVOKANA)]:
            fig.add_trace(go.Scatter(
                x=dfc["month_label"], y=dfc[col_name], name=col_name.title(),
                mode="lines", stackgroup="one",
                line=dict(width=0.5, color=color),
                fillcolor=color,
            ))
        fig.update_layout(**plotly_layout(
            height=300, xaxis_title=None, yaxis_title="%", yaxis=dict(range=[0, 100], gridcolor="#e5e7eb"),
        ))
        st.plotly_chart(fig, use_container_width=True)

    # ── Feedback ──────────────────────────────────────────────
    _feedback_section("market-uptake")


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
