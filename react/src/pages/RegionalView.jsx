import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell } from "recharts";
import { T, fmt, fmtE, pct, mono, sans } from "../theme";
import { REGIONS } from "../data";
import KPI from "../components/KPI";
import Card from "../components/Card";
import Tip from "../components/Tip";
import FeedbackPanel from "../components/FeedbackPanel";

export default function RegionalView({ round }) {
  // Sort by TRx descending
  const sorted = [...REGIONS].sort((a, b) => b.trx - a.trx);
  const totalTrx = sorted.reduce((s, r) => s + r.trx, 0);
  const totalPlan = sorted.reduce((s, r) => s + r.trx_plan, 0);
  const achPct = totalPlan ? ((totalTrx / totalPlan) * 100).toFixed(0) : 0;
  const top3Share = totalTrx ? ((sorted.slice(0, 3).reduce((s, r) => s + r.trx, 0) / totalTrx) * 100).toFixed(0) : 0;

  const chartData = sorted.map((r) => ({
    name: r.region,
    TRx: r.trx,
    Plan: r.trx_plan,
  }));

  const achColor = achPct >= 100 ? "green" : achPct >= 80 ? "yellow" : "red";

  return (
    <div>
      {/* ── KPIs ─────────────────────────────────── */}
      <div style={{ display: "flex", gap: 14, flexWrap: "wrap", marginBottom: 14 }}>
        <KPI label="TRx Gesamt" value={fmt(totalTrx)} sub="alle KV-Regionen · kumuliert" />
        <KPI label="Plan Gesamt" value={fmt(totalPlan)} sub="alle KV-Regionen · kumuliert" />
        <KPI label="Zielerreichung" value={achPct + "%"} sub="Ist / Plan" alert={achColor} />
        <KPI label="Top-3 Konzentration" value={top3Share + "%"} sub="Anteil der 3 stärksten Regionen" />
      </div>

      {/* ── Chart + Table ────────────────────────── */}
      <div style={{ display: "flex", gap: 14, flexWrap: "wrap", marginBottom: 14 }}>
        <Card title="TRx nach KV-Region" sub="Ist vs. Plan — sortiert nach Volumen" flex={2} pageId="regional-view" elementId="region-chart" round={round}>
          <ResponsiveContainer width="100%" height={Math.max(400, sorted.length * 30 + 80)}>
            <BarChart data={chartData} layout="vertical" margin={{ left: 130 }}>
              <CartesianGrid stroke={T.grid} strokeDasharray="3 3" />
              <XAxis type="number" tick={{ fill: T.textMuted, fontSize: 11 }} />
              <YAxis type="category" dataKey="name" tick={{ fill: T.text, fontSize: 11 }} width={125} />
              <Tooltip content={<Tip />} />
              <Bar dataKey="Plan" fill="#374151" opacity={0.25} radius={[0, 4, 4, 0]} barSize={14} />
              <Bar dataKey="TRx" fill={T.accent1} radius={[0, 4, 4, 0]} barSize={14} />
            </BarChart>
          </ResponsiveContainer>
        </Card>

        {/* ── Table ───────────────────────────────── */}
        <Card title="Detail-Tabelle" sub="Performance nach Region" flex={1} pageId="regional-view" elementId="region-table" round={round}>
          <div style={{ overflowX: "auto", maxHeight: 500, overflowY: "auto" }}>
            <table style={{ width: "100%", borderCollapse: "collapse", fontSize: 12, fontFamily: sans }}>
              <thead>
                <tr>
                  {["Region", "TRx", "Plan", "Erzielt", "Net Rev", "MS"].map((h) => (
                    <th
                      key={h}
                      style={{
                        textAlign: h === "Region" ? "left" : "right",
                        padding: "8px 6px",
                        borderBottom: `2px solid ${T.border}`,
                        fontSize: 10,
                        fontWeight: 700,
                        textTransform: "uppercase",
                        color: T.textMuted,
                        fontFamily: mono,
                        position: "sticky",
                        top: 0,
                        background: T.surface,
                      }}
                    >
                      {h}
                    </th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {sorted.map((r) => {
                  const ach = r.trx_plan ? (r.trx / r.trx_plan) * 100 : 0;
                  const achColor = ach >= 100 ? T.green : ach >= 80 ? T.yellow : T.red;
                  return (
                    <tr key={r.region}>
                      <td style={{ padding: "6px", fontWeight: 500, color: T.text }}>{r.region}</td>
                      <td style={{ padding: "6px", textAlign: "right", fontFamily: mono }}>{fmt(r.trx)}</td>
                      <td style={{ padding: "6px", textAlign: "right", fontFamily: mono, color: T.textMuted }}>{fmt(r.trx_plan)}</td>
                      <td style={{ padding: "6px", textAlign: "right", fontFamily: mono, fontWeight: 700, color: achColor }}>
                        {ach.toFixed(0)}%
                      </td>
                      <td style={{ padding: "6px", textAlign: "right", fontFamily: mono }}>{fmtE(r.net_revenue)}</td>
                      <td style={{ padding: "6px", textAlign: "right", fontFamily: mono }}>{r.market_share}%</td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        </Card>
      </div>

      {/* ── Feedback ──────────────────────────────── */}
      <FeedbackPanel pageId="regional-view" round={round} />
    </div>
  );
}
