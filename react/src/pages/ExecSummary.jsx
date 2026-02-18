import { LineChart, Line, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from "recharts";
import { T, fmt, fmtE, dlt, sM } from "../theme";
import { MONTHLY, KPIS } from "../data";
import KPI from "../components/KPI";
import Card from "../components/Card";
import Tip from "../components/Tip";
import FeedbackPanel from "../components/FeedbackPanel";

export default function ExecSummary({ round }) {
  const data = MONTHLY;
  const last = data[data.length - 1];

  // Chart data
  const chartData = data.map((d) => ({
    name: sM(d.month),
    TRx: d.trx,
    Plan: d.trx_plan,
  }));

  const revenueData = data.map((d) => ({
    name: sM(d.month),
    Ist: d.net_revenue,
    Plan: d.net_plan,
  }));

  return (
    <div>
      {/* ── KPIs ─────────────────────────────────── */}
      <div style={{ display: "flex", gap: 14, flexWrap: "wrap", marginBottom: 14 }}>
        <KPI label="Net Revenue kum." value={fmtE(KPIS.cumulative_net_revenue)} sub={"Ziel: €600k"} trend={dlt(KPIS.cumulative_net_revenue, 600000)} />
        <KPI label="TRx kumuliert" value={fmt(KPIS.cumulative_trx)} sub={"Ziel: 8.500"} trend={dlt(KPIS.cumulative_trx, 8500)} />
        <KPI label="Aktive Verordner" value={fmt(KPIS.active_prescribers)} sub={"Ziel: 70"} trend={dlt(KPIS.active_prescribers, 70)} />
        <KPI label="Marktanteil" value={KPIS.market_share_latest + "%"} sub={"Ziel: 25%"} trend={dlt(KPIS.market_share_latest, 25)} />
      </div>

      {/* ── Charts ────────────────────────────────── */}
      <div style={{ display: "flex", gap: 14, flexWrap: "wrap", marginBottom: 14 }}>
        <Card title="TRx Entwicklung" sub="Ist vs. Plan" flex={1} pageId="exec-summary" elementId="trx-chart" round={round}>
          <ResponsiveContainer width="100%" height={260}>
            <LineChart data={chartData}>
              <CartesianGrid stroke={T.grid} strokeDasharray="3 3" />
              <XAxis dataKey="name" tick={{ fill: T.textMuted, fontSize: 11 }} />
              <YAxis tick={{ fill: T.textMuted, fontSize: 11 }} />
              <Tooltip content={<Tip />} />
              <Line type="monotone" dataKey="TRx" stroke={T.accent1} strokeWidth={2.5} dot={{ r: 4 }} />
              <Line type="monotone" dataKey="Plan" stroke={T.textDim} strokeWidth={1.5} strokeDasharray="6 3" dot={false} />
            </LineChart>
          </ResponsiveContainer>
        </Card>

        <Card title="Net Revenue" sub="Monatlich Ist vs. Plan (€)" flex={1} pageId="exec-summary" elementId="revenue-chart" round={round}>
          <ResponsiveContainer width="100%" height={260}>
            <BarChart data={revenueData}>
              <CartesianGrid stroke={T.grid} strokeDasharray="3 3" />
              <XAxis dataKey="name" tick={{ fill: T.textMuted, fontSize: 11 }} />
              <YAxis tick={{ fill: T.textMuted, fontSize: 11 }} />
              <Tooltip content={<Tip />} />
              <Bar dataKey="Ist" fill={T.accent1} radius={[4, 4, 0, 0]} />
              <Bar dataKey="Plan" fill={T.textDim + "44"} radius={[4, 4, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </Card>
      </div>

      {/* ── Feedback ──────────────────────────────── */}
      <FeedbackPanel pageId="exec-summary" round={round} />
    </div>
  );
}
