import { useState } from "react";
import { T, sans, mono } from "./theme";
import { getMaxRound } from "./feedbackStore";
import RoundSelector from "./components/RoundSelector";
import ExecSummary from "./pages/ExecSummary";
import MarketUptake from "./pages/MarketUptake";
import RegionalView from "./pages/RegionalView";
import FeedbackOverview from "./pages/FeedbackOverview";

const PAGES = [
  { id: "exec", label: "Executive Summary", icon: "📊" },
  { id: "uptake", label: "Markt-Uptake", icon: "📈" },
  { id: "regional", label: "Regionale Performance", icon: "🗺" },
  { id: "feedback", label: "Feedback-Übersicht", icon: "💬" },
];

export default function App() {
  const [page, setPage] = useState("exec");
  const [currentRound, setCurrentRound] = useState(1);
  const [maxRound, setMaxRound] = useState(Math.max(1, getMaxRound()));

  const handleAddRound = () => {
    const next = maxRound + 1;
    setMaxRound(next);
    setCurrentRound(next);
  };

  return (
    <div style={{ minHeight: "100vh", background: T.bg, fontFamily: sans }}>
      {/* ── Header ──────────────────────────────── */}
      <header
        style={{
          background: T.surface,
          borderBottom: `1px solid ${T.border}`,
          padding: "14px 24px",
          display: "flex",
          alignItems: "center",
          justifyContent: "space-between",
          flexWrap: "wrap",
          gap: 12,
        }}
      >
        <div>
          <div style={{ fontSize: 17, fontWeight: 700, color: T.text }}>
            Dashboard Prototyper
            <span style={{ fontWeight: 400, color: T.textMuted, fontSize: 13, marginLeft: 8 }}>React-Variante</span>
          </div>
          <div style={{ fontSize: 11, color: T.textDim, fontFamily: mono, marginTop: 2 }}>
            Iteratives Dashboard-Prototyping mit Feedback
          </div>
        </div>
        <RoundSelector
          currentRound={currentRound}
          maxRound={maxRound}
          onSelect={setCurrentRound}
          onAdd={handleAddRound}
        />
      </header>

      {/* ── Tab Navigation ──────────────────────── */}
      <nav
        style={{
          background: T.surface,
          borderBottom: `1px solid ${T.border}`,
          padding: "0 24px",
          display: "flex",
          gap: 0,
          overflowX: "auto",
        }}
      >
        {PAGES.map((p) => (
          <button
            key={p.id}
            onClick={() => setPage(p.id)}
            style={{
              padding: "12px 18px",
              border: "none",
              borderBottom: `2.5px solid ${page === p.id ? T.accent1 : "transparent"}`,
              background: page === p.id ? T.accent1 + "08" : "transparent",
              color: page === p.id ? T.accent1 : T.textMuted,
              fontWeight: page === p.id ? 700 : 500,
              fontSize: 13,
              fontFamily: sans,
              cursor: "pointer",
              whiteSpace: "nowrap",
              transition: "all 0.15s",
            }}
          >
            {p.icon} {p.label}
          </button>
        ))}
      </nav>

      {/* ── Main Content ────────────────────────── */}
      <main style={{ maxWidth: 1200, margin: "0 auto", padding: "20px 24px" }}>
        {page === "exec" && <ExecSummary round={currentRound} />}
        {page === "uptake" && <MarketUptake round={currentRound} />}
        {page === "regional" && <RegionalView round={currentRound} />}
        {page === "feedback" && <FeedbackOverview />}
      </main>

      {/* ── Footer ──────────────────────────────── */}
      <footer style={{ textAlign: "center", padding: "20px", fontSize: 11, color: T.textDim, fontFamily: mono }}>
        Dashboard Prototyper · React + Recharts · Feedback in localStorage
      </footer>
    </div>
  );
}
