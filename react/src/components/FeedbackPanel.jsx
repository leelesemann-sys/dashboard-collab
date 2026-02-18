import { useState } from "react";
import { T, mono, sans } from "../theme";
import { getFeedback, addFeedback, updateStatus } from "../feedbackStore";

export default function FeedbackPanel({ pageId, round }) {
  const [author, setAuthor] = useState("");
  const [comment, setComment] = useState("");
  const [rating, setRating] = useState(3);
  const [refresh, setRefresh] = useState(0);

  const feedback = getFeedback(pageId);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!author.trim() || !comment.trim()) return;
    addFeedback({ pageId, round, author: author.trim(), comment: comment.trim(), rating });
    setAuthor("");
    setComment("");
    setRating(3);
    setRefresh((r) => r + 1);
  };

  const handleToggle = (id) => {
    const item = feedback.find((f) => f.id === id);
    if (item) {
      updateStatus(id, item.status === "open" ? "resolved" : "open");
      setRefresh((r) => r + 1);
    }
  };

  const inputStyle = {
    width: "100%",
    padding: "8px 12px",
    borderRadius: 6,
    border: `1px solid ${T.border}`,
    fontSize: 13,
    fontFamily: sans,
    outline: "none",
    boxSizing: "border-box",
  };

  return (
    <div style={{ marginTop: 24, borderTop: `1px solid ${T.border}`, paddingTop: 20 }}>
      <div style={{ fontSize: 15, fontWeight: 700, color: T.text, fontFamily: sans, marginBottom: 14 }}>
        💬 Feedback zu dieser Seite
      </div>

      {/* ── Form ─────────────────────────────────── */}
      <form onSubmit={handleSubmit} style={{ display: "flex", flexDirection: "column", gap: 10, marginBottom: 20 }}>
        <div style={{ display: "flex", gap: 10, flexWrap: "wrap" }}>
          <input
            style={{ ...inputStyle, flex: 1, minWidth: 160 }}
            placeholder="Dein Name"
            value={author}
            onChange={(e) => setAuthor(e.target.value)}
          />
          <div style={{ display: "flex", alignItems: "center", gap: 2 }}>
            {[1, 2, 3, 4, 5].map((s) => (
              <span
                key={s}
                onClick={() => setRating(s)}
                style={{
                  cursor: "pointer",
                  fontSize: 20,
                  color: s <= rating ? T.yellow : T.border,
                  transition: "color 0.1s",
                }}
              >
                ★
              </span>
            ))}
          </div>
        </div>
        <textarea
          style={{ ...inputStyle, minHeight: 70, resize: "vertical" }}
          placeholder="Dein Kommentar..."
          value={comment}
          onChange={(e) => setComment(e.target.value)}
        />
        <button
          type="submit"
          style={{
            alignSelf: "flex-start",
            padding: "8px 20px",
            borderRadius: 6,
            border: "none",
            background: T.accent1,
            color: "#fff",
            fontWeight: 600,
            fontSize: 13,
            fontFamily: sans,
            cursor: "pointer",
            transition: "opacity 0.15s",
          }}
        >
          📩 Absenden
        </button>
      </form>

      {/* ── History ───────────────────────────────── */}
      {feedback.length > 0 && (
        <div>
          <div style={{ fontSize: 12, fontWeight: 600, color: T.textMuted, textTransform: "uppercase", marginBottom: 8 }}>
            Bisheriges Feedback ({feedback.length})
          </div>
          <div style={{ display: "flex", flexDirection: "column", gap: 8 }}>
            {feedback.map((f) => (
              <div
                key={f.id}
                style={{
                  display: "flex",
                  alignItems: "flex-start",
                  gap: 12,
                  padding: "10px 14px",
                  background: f.status === "resolved" ? T.green + "06" : T.surface2,
                  borderRadius: 8,
                  border: `1px solid ${f.status === "resolved" ? T.green + "22" : T.border}`,
                }}
              >
                <div style={{ flex: 1 }}>
                  <div style={{ display: "flex", alignItems: "center", gap: 8, marginBottom: 4 }}>
                    <span style={{ fontWeight: 600, fontSize: 13, fontFamily: sans }}>{f.author}</span>
                    <span style={{ fontSize: 11, color: T.textMuted, fontFamily: mono }}>Runde {f.round}</span>
                    <span style={{ fontSize: 12, color: T.yellow }}>
                      {"★".repeat(f.rating)}{"☆".repeat(5 - f.rating)}
                    </span>
                  </div>
                  <div style={{ fontSize: 13, color: T.text, lineHeight: 1.5 }}>{f.comment}</div>
                  <div style={{ fontSize: 11, color: T.textDim, fontFamily: mono, marginTop: 4 }}>
                    {new Date(f.created_at).toLocaleString("de-DE")}
                  </div>
                </div>
                <button
                  onClick={() => handleToggle(f.id)}
                  title={f.status === "open" ? "Als erledigt markieren" : "Wieder öffnen"}
                  style={{
                    padding: "4px 10px",
                    borderRadius: 5,
                    border: `1px solid ${f.status === "resolved" ? T.green + "44" : T.border}`,
                    background: f.status === "resolved" ? T.green + "12" : "transparent",
                    color: f.status === "resolved" ? T.green : T.textMuted,
                    fontSize: 12,
                    fontWeight: 600,
                    cursor: "pointer",
                    whiteSpace: "nowrap",
                  }}
                >
                  {f.status === "resolved" ? "✅" : "🔲"}
                </button>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
