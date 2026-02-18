"""
Reusable feedback UI components for all dashboard pages.
Renders styled feedback form + history with HTML cards.
"""
import streamlit as st
from lib import feedback_db
from lib.theme import GREEN, YELLOW, TEXT_DIM


def feedback_section(page_id: str):
    """Render feedback form + styled history for a dashboard page."""
    current_round = st.session_state.get("current_round", 1)

    st.markdown("---")
    st.markdown("#### 💬 Feedback zu dieser Seite")

    with st.form(f"feedback_{page_id}_r{current_round}", clear_on_submit=True):
        fc1, fc2 = st.columns([3, 1])
        author = fc1.text_input("Dein Name", placeholder="z.B. Max Müller")
        rating = fc2.slider("Bewertung", 1, 5, 3)
        comment = st.text_area("Kommentar", placeholder="Was fällt dir auf? Was fehlt? Was sollte anders sein?")
        submitted = st.form_submit_button("📩 Absenden", use_container_width=True)
        if submitted and author.strip() and comment.strip():
            feedback_db.add_feedback(page_id, current_round, author.strip(), comment.strip(), rating)
            st.rerun()

    # ── History (HTML styled) ─────────────────────────────────
    df_fb = feedback_db.get_feedback(page_id=page_id)
    if not df_fb.empty:
        st.markdown(f"""<div style="font-size:12px; font-weight:600; color:#6b7280;
            text-transform:uppercase; margin: 16px 0 8px 0; letter-spacing:0.5px;">
            Bisheriges Feedback ({len(df_fb)})
        </div>""", unsafe_allow_html=True)

        for _, row in df_fb.iterrows():
            stars = "★" * int(row["rating"]) + "☆" * (5 - int(row["rating"]))
            is_resolved = row["status"] == "resolved"
            css_class = "feedback-item resolved" if is_resolved else "feedback-item"
            time_str = str(row["created_at"])[:16].replace("T", " ")

            st.markdown(f"""
            <div class="{css_class}">
                <div style="flex:1">
                    <div style="display:flex; align-items:center; gap:8px; margin-bottom:4px;">
                        <span class="feedback-author">{row['author']}</span>
                        <span class="feedback-round">Runde {row['round']}</span>
                        <span class="feedback-stars">{stars}</span>
                    </div>
                    <div class="feedback-comment">{row['comment']}</div>
                    <div class="feedback-time">{time_str}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Status toggle button (needs Streamlit widget)
            col_spacer, col_btn = st.columns([6, 1])
            with col_btn:
                btn_label = "✅ Erledigt" if is_resolved else "🔲 Offen"
                if st.button(btn_label, key=f"toggle_{page_id}_{row['id']}", use_container_width=True):
                    new_status = "resolved" if row["status"] == "open" else "open"
                    feedback_db.update_status(int(row["id"]), new_status)
                    st.rerun()
