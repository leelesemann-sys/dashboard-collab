import { useState } from "react";
import { T, mono, sans } from "../theme";
import { getFeedback, exportCSV, exportJSON, updateStatus, getAllElementIds } from "../feedbackStore";
import KPI from "../components/KPI";
import Card from "../components/Card";

export default function FeedbackOverview() {
  const [filterRound, setFilterRound] = useState("");
  const [filterPage, setFilterPage] = useState("");
  const [filterElement, setFilterElement] = useState("");
  const [filterStatus, setFilterStatus] = useState("");
  const [refresh, setRefresh] = useState(0);

  let feedback = getFeedback();

  // Derive filter options
  const allRounds = [...new Set(feedback.map((f) => f.round))].sort();
  const allPages = [...new Set(feedback.map((f) => f.page_id))].sort();
  const allElements = [...new Set(feedback.filter((f) => f.element_id).map((f) => f.element_id))].sort();

  // Apply filters
  if (filterRound) feedback = feedback.filter((f) => f.round === Number(filterRound));
  if (filterPage) feedback = feedback.filter((f) => f.page_id === filterPage);
  if (filterElement === "__page__") feedback = feedback.filter((f) => !f.element_id);
  else if (filterElement) feedback = feedback.filter((f) => f.element_id === filterElement);
  if (filterStatus) feedback = feedback.filter((f) => f.status === filterStatus);

  // Stats
  const total = feedback.length;
  const avgRating = total ? (feedback.reduce((s, f) => s + f.rating, 0) / total).toFixed(1) : "–";
  const openCount = feedback.filter((f) => f.status === "open").length;
  const resolvedCount = feedback.filter((f) => f.status === "resolved").length;

  const handleToggle = (id) => {
    const item = feedback.find((f) => f.id === id);
    if (item) {
      updateStatus(id, item.status === "open" ? "resolved" : "open");
      setRefresh((r) => r + 1);
    }
  };

  const selectStyle = {
    padding: "6px 10px",
    borderRadius: 6,
    border: `1px solid ${T.border}`,
    fontSize: 12,
    fontFamily: sans,
    background: T.surface,
    color: T.text,
    outline: "none",
  };

  const btnStyle = {
    padding: "8px 16px",
    borderRadius: 6,
    border: `1px solid ${T.border}`,
    background: T.surface,
    fontSize: 12,
    fontWeight: 600,
    fontFamily: sans,
    cursor: "pointer",
    transition: "all 0.15s",
  };

  return (
    <div>
      {/* ── Stats ─────────────────────────────────── */}
      <div style={{ display: "flex", gap: 14, flexWrap: "wrap", marginBottom: 14 }}>
        <KPI label="Gesamt" value={String(total)} />
        <KPI label="Ø Bewertung" value={avgRating + " ★"} />
        <KPI label="Offen" value={String(openCount)} alert={openCount > 0 ? "yellow" : null} />
        <KPI label="Erledigt" value={String(resolvedCount)} />
      </div>

      {/* ── Filters + Export ──────────────────────── */}
      <Card style={{ marginBottom: 14 }}>
        <div style={{ display: "flex", alignItems: "center", gap: 12, flexWrap: "wrap" }}>
          <select style={selectStyle} value={filterRound} onChange={(e) => setFilterRound(e.target.value)}>
            <option value="">Alle Runden</option>
            {allRounds.map((r) => (
              <option key={r} value={r}>Runde {r}</option>
            ))}
          </select>
          <select style={selectStyle} value={filterPage} onChange={(e) => setFilterPage(e.target.value)}>
            <option value="">Alle Seiten</option>
            {allPages.map((p) => (
              <option key={p} value={p}>{p}</option>
            ))}
          </select>
          <select style={selectStyle} value={filterElement} onChange={(e) => setFilterElement(e.target.value)}>
            <option value="">Alle Elemente</option>
            <option value="__page__">Nur Seitenkommentare</option>
            {allElements.map((e) => (
              <option key={e} value={e}>{e}</option>
            ))}
          </select>
          <select style={selectStyle} value={filterStatus} onChange={(e) => setFilterStatus(e.target.value)}>
            <option value="">Alle Status</option>
            <option value="open">Offen</option>
            <option value="resolved">Erledigt</option>
          </select>
          <div style={{ flex: 1 }} />
          <button style={btnStyle} onClick={exportCSV}>📥 CSV</button>
          <button style={btnStyle} onClick={exportJSON}>📥 JSON</button>
        </div>
      </Card>

      {/* ── Table ─────────────────────────────────── */}
      <Card>
        {feedback.length === 0 ? (
          <div style={{ textAlign: "center", padding: 40, color: T.textMuted, fontSize: 14 }}>
            Noch kein Feedback vorhanden.
          </div>
        ) : (
          <div style={{ overflowX: "auto" }}>
            <table style={{ width: "100%", borderCollapse: "collapse", fontSize: 12, fontFamily: sans }}>
              <thead>
                <tr>
                  {["Runde", "Seite", "Element", "Autor", "Kommentar", "Bewertung", "Status", "Datum"].map((h) => (
                    <th
                      key={h}
                      style={{
                        textAlign: "left",
                        padding: "8px 8px",
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
                {feedback.map((f) => (
                  <tr key={f.id} style={{ borderBottom: `1px solid ${T.border}` }}>
                    <td style={{ padding: "8px", fontFamily: mono, fontWeight: 600 }}>{f.round}</td>
                    <td style={{ padding: "8px" }}>{f.page_id}</td>
                    <td style={{ padding: "8px" }}>
                      {f.element_id ? (
                        <span style={{
                          fontSize: 10, fontFamily: mono, background: T.accent1 + "12",
                          color: T.accent1, padding: "2px 6px", borderRadius: 3, fontWeight: 600,
                        }}>
                          {f.element_id}
                        </span>
                      ) : (
                        <span style={{ fontSize: 10, color: T.textDim }}>Seite</span>
                      )}
                    </td>
                    <td style={{ padding: "8px", fontWeight: 500 }}>{f.author}</td>
                    <td style={{ padding: "8px", maxWidth: 280, color: T.text, lineHeight: 1.4 }}>{f.comment}</td>
                    <td style={{ padding: "8px", color: T.yellow }}>
                      {"★".repeat(f.rating)}{"☆".repeat(5 - f.rating)}
                    </td>
                    <td style={{ padding: "8px" }}>
                      <button
                        onClick={() => handleToggle(f.id)}
                        style={{
                          padding: "3px 8px",
                          borderRadius: 4,
                          border: `1px solid ${f.status === "resolved" ? T.green + "44" : T.yellow + "44"}`,
                          background: f.status === "resolved" ? T.green + "12" : T.yellow + "12",
                          color: f.status === "resolved" ? T.green : T.yellow,
                          fontSize: 11,
                          fontWeight: 600,
                          cursor: "pointer",
                        }}
                      >
                        {f.status === "resolved" ? "✅ Erledigt" : "🔲 Offen"}
                      </button>
                    </td>
                    <td style={{ padding: "8px", fontFamily: mono, fontSize: 11, color: T.textDim }}>
                      {new Date(f.created_at).toLocaleString("de-DE")}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </Card>
    </div>
  );
}
