"""Feedback Overview — Admin page with filters, table, and export."""
import streamlit as st
import pandas as pd
from io import BytesIO

from lib import feedback_db
from lib.theme import ACCENT1, GREEN, YELLOW


def show():
    st.header("💬 Feedback-Übersicht")

    # ── Load all feedback ─────────────────────────────────────
    df_all = feedback_db.export_dataframe()

    if df_all.empty:
        st.info("Noch kein Feedback vorhanden. Gib auf den Dashboard-Seiten Feedback ab!")
        return

    # ── Stats KPIs ────────────────────────────────────────────
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Gesamt", len(df_all))
    c2.metric("Ø Bewertung", f"{df_all['rating'].mean():.1f} ★")
    c3.metric("Offen", len(df_all[df_all["status"] == "open"]))
    c4.metric("Erledigt", len(df_all[df_all["status"] == "resolved"]))

    st.markdown("---")

    # ── Filters ───────────────────────────────────────────────
    fc1, fc2, fc3, fc4 = st.columns([1, 1, 1, 2])

    rounds = sorted(df_all["round"].unique())
    round_filter = fc1.selectbox("Runde", ["Alle"] + [f"Runde {r}" for r in rounds])

    pages = sorted(df_all["page_id"].unique())
    page_filter = fc2.selectbox("Seite", ["Alle"] + pages)

    status_filter = fc3.selectbox("Status", ["Alle", "Offen", "Erledigt"])

    # Apply filters
    df_filtered = df_all.copy()
    if round_filter != "Alle":
        r_num = int(round_filter.split(" ")[1])
        df_filtered = df_filtered[df_filtered["round"] == r_num]
    if page_filter != "Alle":
        df_filtered = df_filtered[df_filtered["page_id"] == page_filter]
    if status_filter == "Offen":
        df_filtered = df_filtered[df_filtered["status"] == "open"]
    elif status_filter == "Erledigt":
        df_filtered = df_filtered[df_filtered["status"] == "resolved"]

    # ── Export buttons ────────────────────────────────────────
    with fc4:
        st.write("")  # spacing
        exp1, exp2 = st.columns(2)
        csv = df_filtered.to_csv(index=False).encode("utf-8")
        exp1.download_button("📥 CSV", csv, "feedback.csv", "text/csv", use_container_width=True)

        buffer = BytesIO()
        df_filtered.to_excel(buffer, index=False, engine="openpyxl")
        exp2.download_button("📥 Excel", buffer.getvalue(), "feedback.xlsx",
                             "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                             use_container_width=True)

    # ── Feedback table ────────────────────────────────────────
    st.subheader(f"Feedback ({len(df_filtered)} Einträge)")

    if df_filtered.empty:
        st.info("Keine Einträge für die gewählten Filter.")
        return

    for _, row in df_filtered.iterrows():
        stars = "★" * int(row["rating"]) + "☆" * (5 - int(row["rating"]))
        status_icon = "✅" if row["status"] == "resolved" else "🔲"
        border_color = GREEN if row["status"] == "resolved" else YELLOW

        with st.container(border=True):
            hc1, hc2, hc3, hc4, hc5 = st.columns([1, 1, 3, 1, 1])
            hc1.markdown(f"`Runde {row['round']}`")
            hc2.markdown(f"**{row['author']}**")
            hc3.write(row["comment"])
            hc4.write(f"{stars}")
            if hc5.button(status_icon, key=f"admin_toggle_{row['id']}"):
                new_status = "resolved" if row["status"] == "open" else "open"
                feedback_db.update_status(int(row["id"]), new_status)
                st.rerun()

        # Show metadata
        st.caption(f"📄 {row['page_id']} · 🕐 {row['created_at'][:16]}")
