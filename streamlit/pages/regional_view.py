"""Regional Performance — Horizontal bars + Detail table."""
import streamlit as st
import plotly.graph_objects as go

from lib.mock_data import df_regions
from lib.theme import ACCENT1, ACCENT2, TEXT_DIM, GREEN, YELLOW, RED, plotly_layout, render_kpis
from lib.feedback_ui import section_with_feedback, feedback_section


def show():
    st.markdown("## 🗺 Regionale Performance")

    df = df_regions.sort_values("trx", ascending=False).copy()
    total_trx = int(df["trx"].sum())
    total_plan = int(df["trx_plan"].sum())
    ach_pct = total_trx / total_plan * 100 if total_plan else 0
    top3_share = df.head(3)["trx"].sum() / total_trx * 100 if total_trx else 0

    # ── KPIs ──────────────────────────────────────────────────
    render_kpis(st.columns(4), [
        {"label": "TRx Gesamt", "value": f"{total_trx:,}",
         "sub": "alle KV-Regionen · kumuliert"},
        {"label": "Plan Gesamt", "value": f"{total_plan:,}",
         "sub": "alle KV-Regionen · kumuliert"},
        {"label": "Zielerreichung", "value": f"{ach_pct:.0f}%",
         "sub": "Ist / Plan",
         "trend_color": GREEN if ach_pct >= 100 else YELLOW if ach_pct >= 80 else RED},
        {"label": "Top-3 Konzentration", "value": f"{top3_share:.0f}%",
         "sub": "Anteil der 3 stärksten Regionen"},
    ])

    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

    # ── Chart + Table ─────────────────────────────────────────
    col1, col2 = st.columns([3, 2])

    with col1:
        section_with_feedback("regional-view", "region-chart", "TRx nach KV-Region", "Ist vs. Plan — sortiert nach Volumen")

        df_chart = df.sort_values("trx", ascending=True)

        fig = go.Figure()
        # Plan bars first (behind) — darker, clear benchmark style
        fig.add_trace(go.Bar(
            y=df_chart["region"], x=df_chart["trx_plan"], name="Plan",
            orientation="h", marker_color="#374151", opacity=0.25,
            marker_cornerradius=4,
        ))
        # Actual bars on top
        fig.add_trace(go.Bar(
            y=df_chart["region"], x=df_chart["trx"], name="Ist",
            orientation="h", marker_color=ACCENT1, marker_cornerradius=4,
        ))
        fig.update_layout(**plotly_layout(
            height=max(400, len(df_chart) * 30 + 80),
            barmode="overlay",
            margin=dict(l=160, r=20, t=36, b=44),
        ))
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    with col2:
        section_with_feedback("regional-view", "region-table", "Detail-Tabelle", "Performance nach Region")

        # Build styled HTML table
        rows_html = ""
        for _, r in df.iterrows():
            ach = r["trx"] / r["trx_plan"] * 100 if r["trx_plan"] else 0
            ach_color = GREEN if ach >= 100 else YELLOW if ach >= 80 else RED
            net_fmt = f"€{r['net_revenue']:,.0f}"
            rows_html += f"""<tr>
                <td style="padding:6px 8px; font-weight:500">{r['region']}</td>
                <td style="padding:6px 8px; text-align:right; font-family:'JetBrains Mono',mono; font-size:12px">{r['trx']:,.0f}</td>
                <td style="padding:6px 8px; text-align:right; font-family:'JetBrains Mono',mono; font-size:12px; color:#6b7280">{r['trx_plan']:,.0f}</td>
                <td style="padding:6px 8px; text-align:right; font-family:'JetBrains Mono',mono; font-size:12px; font-weight:700; color:{ach_color}">{ach:.0f}%</td>
                <td style="padding:6px 8px; text-align:right; font-family:'JetBrains Mono',mono; font-size:12px">{net_fmt}</td>
                <td style="padding:6px 8px; text-align:right; font-family:'JetBrains Mono',mono; font-size:12px">{r['market_share']}%</td>
            </tr>"""

        st.markdown(f"""
        <div style="overflow-x:auto; font-family:'DM Sans',sans-serif; font-size:13px; max-height:500px; overflow-y:auto;">
            <table style="width:100%; border-collapse:collapse;">
                <thead>
                    <tr style="border-bottom:2px solid #e2e5ea; position:sticky; top:0; background:#ffffff;">
                        <th style="padding:8px 8px; text-align:left; font-size:10px; font-weight:700; text-transform:uppercase; color:#6b7280; font-family:'JetBrains Mono',mono; letter-spacing:0.5px">Region</th>
                        <th style="padding:8px 8px; text-align:right; font-size:10px; font-weight:700; text-transform:uppercase; color:#6b7280; font-family:'JetBrains Mono',mono">TRx</th>
                        <th style="padding:8px 8px; text-align:right; font-size:10px; font-weight:700; text-transform:uppercase; color:#6b7280; font-family:'JetBrains Mono',mono">Plan</th>
                        <th style="padding:8px 8px; text-align:right; font-size:10px; font-weight:700; text-transform:uppercase; color:#6b7280; font-family:'JetBrains Mono',mono">Erzielt</th>
                        <th style="padding:8px 8px; text-align:right; font-size:10px; font-weight:700; text-transform:uppercase; color:#6b7280; font-family:'JetBrains Mono',mono">Net Rev</th>
                        <th style="padding:8px 8px; text-align:right; font-size:10px; font-weight:700; text-transform:uppercase; color:#6b7280; font-family:'JetBrains Mono',mono">MS</th>
                    </tr>
                </thead>
                <tbody>{rows_html}</tbody>
            </table>
        </div>
        """, unsafe_allow_html=True)

    # ── Feedback ──────────────────────────────────────────────
    feedback_section("regional-view")
