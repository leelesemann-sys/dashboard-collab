"""
Reusable feedback UI components for all dashboard pages.
Supports both page-level and element-level feedback.
"""
import streamlit as st
from lib import feedback_db
from lib.theme import GREEN, YELLOW, TEXT_DIM, ACCENT1


def element_feedback(page_id: str, element_id: str, label: str):
    """Render a compact element-level feedback widget using st.popover."""
    current_round = st.session_state.get("current_round", 1)
    count = feedback_db.get_element_count(page_id, element_id)

    badge = f"💬 {count}" if count > 0 else "💬"
    with st.popover(badge, use_container_width=False):
        st.markdown(f"**Feedback:** {label}")
        with st.form(f"ef_{page_id}_{element_id}_r{current_round}", clear_on_submit=True):
            author = st.text_input("Name", placeholder="Dein Name", key=f"ef_a_{page_id}_{element_id}")
            comment = st.text_area("Kommentar", placeholder="Was fällt dir auf?", key=f"ef_c_{page_id}_{element_id}", height=80)
            rating = st.slider("Bewertung", 1, 5, 3, key=f"ef_r_{page_id}_{element_id}")
            if st.form_submit_button("Absenden", use_container_width=True):
                if author.strip() and comment.strip():
                    feedback_db.add_feedback(page_id, current_round, author.strip(), comment.strip(), rating, element_id)
                    st.rerun()

        # Show existing feedback for this element
        df = feedback_db.get_feedback(page_id=page_id, element_id=element_id)
        if not df.empty:
            st.markdown(f"---\n**{len(df)} Kommentar{'e' if len(df) != 1 else ''}:**")
            for _, row in df.iterrows():
                stars = "★" * int(row["rating"])
                status_icon = "✅" if row["status"] == "resolved" else "🔲"
                st.markdown(f"{status_icon} **{row['author']}** (R{row['round']}) {stars}  \n{row['comment']}")


def section_with_feedback(page_id: str, element_id: str, title: str, subtitle: str = ""):
    """Render a section header row with title and element feedback bubble."""
    col_title, col_fb = st.columns([6, 1])
    with col_title:
        st.markdown(f"""<div class="section-card" style="margin-bottom:0; border-bottom:none; border-radius:10px 10px 0 0;">
            <div class="section-title">{title}</div>
            {"<div class='section-sub'>" + subtitle + "</div>" if subtitle else ""}
        """, unsafe_allow_html=True)
    with col_fb:
        element_feedback(page_id, element_id, title)
    return col_title


def close_section():
    """Close a section card opened by section_with_feedback."""
    st.markdown("</div>", unsafe_allow_html=True)


def feedback_section(page_id: str):
    """Render page-level feedback form + styled history."""
    current_round = st.session_state.get("current_round", 1)

    st.markdown("---")
    st.markdown("#### 💬 Allgemeines Feedback zur Seite")

    with st.form(f"feedback_{page_id}_r{current_round}", clear_on_submit=True):
        fc1, fc2 = st.columns([3, 1])
        author = fc1.text_input("Dein Name", placeholder="z.B. Max Müller")
        rating = fc2.slider("Bewertung", 1, 5, 3)
        comment = st.text_area("Kommentar", placeholder="Layout, fehlende Elemente, Reihenfolge...")
        submitted = st.form_submit_button("📩 Absenden", use_container_width=True)
        if submitted and author.strip() and comment.strip():
            feedback_db.add_feedback(page_id, current_round, author.strip(), comment.strip(), rating)
            st.rerun()

    # History: page-level only (element_id IS NULL)
    df_fb = feedback_db.get_feedback(page_id=page_id, element_id=None)
    if not df_fb.empty:
        st.markdown(f"""<div style="font-size:12px; font-weight:600; color:#6b7280;
            text-transform:uppercase; margin: 16px 0 8px 0; letter-spacing:0.5px;">
            Seitenkommentare ({len(df_fb)})
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

            col_spacer, col_btn = st.columns([6, 1])
            with col_btn:
                btn_label = "✅ Erledigt" if is_resolved else "🔲 Offen"
                if st.button(btn_label, key=f"toggle_{page_id}_{row['id']}", use_container_width=True):
                    new_status = "resolved" if row["status"] == "open" else "open"
                    feedback_db.update_status(int(row["id"]), new_status)
                    st.rerun()
