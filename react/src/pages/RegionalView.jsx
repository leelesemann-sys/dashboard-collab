import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell } from "recharts";
import { T, fmt, fmtE, pct, mono, sans } from "../theme";
import { REGIONS } from "../data";
import Card from "../components/Card";
import Tip from "../components/Tip";
import FeedbackPanel from "../components/FeedbackPanel";

export default function RegionalView({ round }) {
  // Sort by TRx descending
  const sorted = [...REGIONS].sort((a, b) => b.trx - a.trx);

  const chartData = sorted.map((r) => ({
    name: r.region,
    TRx: r.trx,
    Plan: r.trx_plan,
  }));

  return (
    <div>
      {/* ── Chart ─────────────────────────────────── */}
      <div style={{ display: "flex", gap: 14, flexWrap: "wrap", marginBottom: 14 }}>
        <Card title="TRx nach KV-Region" sub="Ist vs. Plan" flex={2}>
          <ResponsiveContainer width="100%" height={360}>
            <BarChart data={chartData} layout="vertical" margin={{ left: 100 }}>
              <CartesianGrid stroke={T.grid} strokeDasharray="3 3" />
              <XAxis type="number" tick={{ fill: T.textMuted, fontSize: 11 }} />
              <YAxis type="category" dataKey="name" tick={{ fill: T.text, fontSize: 12 }} width={95} />
              <Tooltip content={<Tip />} />
              <Bar dataKey="TRx" fill={T.accent1} radius={[0, 4, 4, 0]} barSize={14} />
              <Bar dataKey="Plan" fill={T.textDim + "44"} radius={[0, 4, 4, 0]} barSize={14} />
            </BarChart>
          </ResponsiveContainer>
        </Card>

        {/* ── Table ───────────────────────────────── */}
        <Card title="Detail-Tabelle" sub="Performance nach Region" flex={1}>
          <div style={{ overflowX: "auto" }}>
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
