"""Feedback Overview — Admin page with filters, styled table, and export."""
import streamlit as st
from io import BytesIO

from lib import feedback_db
from lib.theme import GREEN, YELLOW, RED, render_kpis


def show():
    st.markdown("## 💬 Feedback-Übersicht")

    df_all = feedback_db.export_dataframe()

    if df_all.empty:
        st.markdown("""<div class="section-card" style="text-align:center; padding:40px;">
            <div style="font-size:32px; margin-bottom:8px">📋</div>
            <div style="font-size:14px; color:#6b7280">Noch kein Feedback vorhanden.</div>
            <div style="font-size:13px; color:#9ca3af; margin-top:4px">Gib auf den Dashboard-Seiten Feedback ab!</div>
        </div>""", unsafe_allow_html=True)
        return

    # ── Stats KPIs ────────────────────────────────────────────
    open_count = len(df_all[df_all["status"] == "open"])
    resolved_count = len(df_all[df_all["status"] == "resolved"])
    avg_rating = df_all["rating"].mean()

    render_kpis(st.columns(4), [
        {"label": "Gesamt", "value": str(len(df_all))},
        {"label": "Ø Bewertung", "value": f"{avg_rating:.1f} ★", "trend_color": YELLOW},
        {"label": "Offen", "value": str(open_count),
         "trend_color": RED if open_count > 0 else GREEN},
        {"label": "Erledigt", "value": str(resolved_count), "trend_color": GREEN},
    ])

    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

    # ── Filters + Export ──────────────────────────────────────
    st.markdown("""<div class="section-card">
        <div class="section-title">Filter & Export</div>
    """, unsafe_allow_html=True)

    fc1, fc2, fc3, fc4 = st.columns([1, 1, 1, 2])

    rounds = sorted(df_all["round"].unique())
    round_filter = fc1.selectbox("Runde", ["Alle"] + [f"Runde {r}" for r in rounds])

    pages = sorted(df_all["page_id"].unique())
    page_filter = fc2.selectbox("Seite", ["Alle"] + pages)

    status_filter = fc3.selectbox("Status", ["Alle", "Offen", "Erledigt"])

    # Apply filters
    df = df_all.copy()
    if round_filter != "Alle":
        df = df[df["round"] == int(round_filter.split(" ")[1])]
    if page_filter != "Alle":
        df = df[df["page_id"] == page_filter]
    if status_filter == "Offen":
        df = df[df["status"] == "open"]
    elif status_filter == "Erledigt":
        df = df[df["status"] == "resolved"]

    with fc4:
        st.write("")
        exp1, exp2 = st.columns(2)
        csv = df.to_csv(index=False).encode("utf-8")
        exp1.download_button("📥 CSV", csv, "feedback.csv", "text/csv", use_container_width=True)
        buffer = BytesIO()
        df.to_excel(buffer, index=False, engine="openpyxl")
        exp2.download_button("📥 Excel", buffer.getvalue(), "feedback.xlsx",
                             "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                             use_container_width=True)

    st.markdown("</div>", unsafe_allow_html=True)

    # ── Feedback entries (HTML styled) ────────────────────────
    st.markdown(f"""<div style="font-size:12px; font-weight:600; color:#6b7280;
        text-transform:uppercase; margin:16px 0 8px 0; letter-spacing:0.5px">
        {len(df)} Einträge
    </div>""", unsafe_allow_html=True)

    for _, row in df.iterrows():
        stars = "★" * int(row["rating"]) + "☆" * (5 - int(row["rating"]))
        is_resolved = row["status"] == "resolved"
        css_class = "feedback-item resolved" if is_resolved else "feedback-item"
        time_str = str(row["created_at"])[:16].replace("T", " ")

        st.markdown(f"""
        <div class="{css_class}">
            <div style="flex:1">
                <div style="display:flex; align-items:center; gap:8px; flex-wrap:wrap; margin-bottom:4px;">
                    <span style="font-family:'JetBrains Mono',mono; font-size:11px; font-weight:600;
                        background:#2563eb12; color:#2563eb; padding:2px 8px; border-radius:4px;">Runde {row['round']}</span>
                    <span style="font-size:11px; color:#6b7280; background:#f0f2f5; padding:2px 8px; border-radius:4px;">📄 {row['page_id']}</span>
                    <span class="feedback-author">{row['author']}</span>
                    <span class="feedback-stars">{stars}</span>
                </div>
                <div class="feedback-comment">{row['comment']}</div>
                <div class="feedback-time">{time_str}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Toggle button
        col_spacer, col_btn = st.columns([6, 1])
        with col_btn:
            btn_label = "✅ Erledigt" if is_resolved else "🔲 Offen"
            if st.button(btn_label, key=f"admin_toggle_{row['id']}", use_container_width=True):
                new_status = "resolved" if row["status"] == "open" else "open"
                feedback_db.update_status(int(row["id"]), new_status)
                st.rerun()
