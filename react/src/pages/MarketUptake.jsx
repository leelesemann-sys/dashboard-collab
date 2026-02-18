import { ComposedChart, Bar, Area, AreaChart, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend } from "recharts";
import { T, fmt, sM } from "../theme";
import { MONTHLY, COMPETITORS } from "../data";
import KPI from "../components/KPI";
import Card from "../components/Card";
import Tip from "../components/Tip";
import FeedbackPanel from "../components/FeedbackPanel";

export default function MarketUptake({ round }) {
  // NRx / RRx stacked bars
  const uptakeData = MONTHLY.map((d) => ({
    name: sM(d.month),
    NRx: d.nrx,
    RRx: d.rrx,
  }));

  // Competitor market shares
  const compData = COMPETITORS.map((d) => ({
    name: sM(d.month),
    Forxiga: d.forxiga,
    Jardiance: d.jardiance,
    Invokana: d.invokana,
    Cardiozan: d.cardiozan,
  }));

  const last = MONTHLY[MONTHLY.length - 1];
  const cumNrx = MONTHLY.reduce((s, d) => s + d.nrx, 0);
  const cumRrx = MONTHLY.reduce((s, d) => s + d.rrx, 0);
  const repeatRatio = cumRrx > 0 ? ((cumRrx / (cumNrx + cumRrx)) * 100).toFixed(1) + "%" : "0%";

  return (
    <div>
      {/* ── KPIs ─────────────────────────────────── */}
      <div style={{ display: "flex", gap: 14, flexWrap: "wrap", marginBottom: 14 }}>
        <KPI label="NRx kumuliert" value={fmt(cumNrx)} />
        <KPI label="RRx kumuliert" value={fmt(cumRrx)} />
        <KPI label="Repeat-Rate" value={repeatRatio} />
        <KPI label="Verordner aktuell" value={fmt(last.prescribers)} />
      </div>

      {/* ── Charts ────────────────────────────────── */}
      <div style={{ display: "flex", gap: 14, flexWrap: "wrap", marginBottom: 14 }}>
        <Card title="NRx vs. RRx" sub="Neue vs. wiederholte Verordnungen" flex={1}>
          <ResponsiveContainer width="100%" height={260}>
            <ComposedChart data={uptakeData}>
              <CartesianGrid stroke={T.grid} strokeDasharray="3 3" />
              <XAxis dataKey="name" tick={{ fill: T.textMuted, fontSize: 11 }} />
              <YAxis tick={{ fill: T.textMuted, fontSize: 11 }} />
              <Tooltip content={<Tip />} />
              <Legend wrapperStyle={{ fontSize: 12 }} />
              <Bar dataKey="NRx" stackId="a" fill={T.accent1} radius={[0, 0, 0, 0]} />
              <Bar dataKey="RRx" stackId="a" fill={T.accent2} radius={[4, 4, 0, 0]} />
            </ComposedChart>
          </ResponsiveContainer>
        </Card>

        <Card title="Marktanteile SGLT2i" sub="Monatliche Entwicklung (%)" flex={1}>
          <ResponsiveContainer width="100%" height={260}>
            <AreaChart data={compData}>
              <CartesianGrid stroke={T.grid} strokeDasharray="3 3" />
              <XAxis dataKey="name" tick={{ fill: T.textMuted, fontSize: 11 }} />
              <YAxis tick={{ fill: T.textMuted, fontSize: 11 }} domain={[0, 100]} />
              <Tooltip content={<Tip />} />
              <Legend wrapperStyle={{ fontSize: 12 }} />
              <Area type="monotone" dataKey="Cardiozan" stackId="1" fill={T.accent1} stroke={T.accent1} fillOpacity={0.7} />
              <Area type="monotone" dataKey="Forxiga" stackId="1" fill="#64748b" stroke="#64748b" fillOpacity={0.5} />
              <Area type="monotone" dataKey="Jardiance" stackId="1" fill="#78716c" stroke="#78716c" fillOpacity={0.5} />
              <Area type="monotone" dataKey="Invokana" stackId="1" fill="#94a3b8" stroke="#94a3b8" fillOpacity={0.5} />
            </AreaChart>
          </ResponsiveContainer>
        </Card>
      </div>

      {/* ── Feedback ──────────────────────────────── */}
      <FeedbackPanel pageId="market-uptake" round={round} />
    </div>
  );
}
