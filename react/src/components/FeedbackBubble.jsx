import { useState, useRef, useEffect } from "react";
import { T, mono, sans } from "../theme";
import { getFeedback, addFeedback, updateStatus, getElementCount } from "../feedbackStore";

export default function FeedbackBubble({ pageId, elementId, round }) {
  const [open, setOpen] = useState(false);
  const [author, setAuthor] = useState("");
  const [comment, setComment] = useState("");
  const [rating, setRating] = useState(3);
  const [refresh, setRefresh] = useState(0);
  const popRef = useRef(null);

  const count = getElementCount(pageId, elementId);
  const feedback = open ? getFeedback(pageId, undefined, elementId) : [];

  // Close on outside click
  useEffect(() => {
    if (!open) return;
    const handler = (e) => {
      if (popRef.current && !popRef.current.contains(e.target)) setOpen(false);
    };
    document.addEventListener("mousedown", handler);
    return () => document.removeEventListener("mousedown", handler);
  }, [open]);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!author.trim() || !comment.trim()) return;
    addFeedback({ pageId, elementId, round, author: author.trim(), comment: comment.trim(), rating });
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

  return (
    <div style={{ position: "relative", display: "inline-flex" }}>
      {/* ── Trigger Button ─────────────────────── */}
      <button
        onClick={() => setOpen(!open)}
        style={{
          display: "inline-flex",
          alignItems: "center",
          gap: 4,
          padding: "3px 8px",
          borderRadius: 5,
          border: `1px solid ${open ? T.accent1 + "44" : T.border}`,
          background: open ? T.accent1 + "10" : count > 0 ? T.yellow + "10" : "transparent",
          color: count > 0 ? T.yellow : T.textDim,
          fontSize: 12,
          fontWeight: 600,
          fontFamily: sans,
          cursor: "pointer",
          transition: "all 0.15s",
        }}
        title={`${count} Kommentar${count !== 1 ? "e" : ""}`}
      >
        💬{count > 0 && <span style={{ fontFamily: mono, fontSize: 11 }}>{count}</span>}
      </button>

      {/* ── Popover ────────────────────────────── */}
      {open && (
        <div
          ref={popRef}
          style={{
            position: "absolute",
            top: "100%",
            right: 0,
            marginTop: 6,
            width: 340,
            background: T.surface,
            border: `1px solid ${T.border}`,
            borderRadius: 10,
            boxShadow: "0 8px 32px rgba(0,0,0,0.12)",
            zIndex: 1000,
            padding: 16,
            maxHeight: 480,
            overflowY: "auto",
          }}
        >
          <div style={{ fontSize: 13, fontWeight: 700, color: T.text, marginBottom: 10 }}>
            💬 Feedback: <span style={{ fontWeight: 400, color: T.textMuted }}>{elementId}</span>
          </div>

          {/* ── Mini Form ──────────────────────── */}
          <form onSubmit={handleSubmit} style={{ display: "flex", flexDirection: "column", gap: 8, marginBottom: feedback.length > 0 ? 14 : 0 }}>
            <input
              style={{
                width: "100%", padding: "6px 10px", borderRadius: 5,
                border: `1px solid ${T.border}`, fontSize: 12, fontFamily: sans,
                outline: "none", boxSizing: "border-box",
              }}
              placeholder="Dein Name"
              value={author}
              onChange={(e) => setAuthor(e.target.value)}
            />
            <textarea
              style={{
                width: "100%", padding: "6px 10px", borderRadius: 5,
                border: `1px solid ${T.border}`, fontSize: 12, fontFamily: sans,
                outline: "none", boxSizing: "border-box", minHeight: 50, resize: "vertical",
              }}
              placeholder="Kommentar..."
              value={comment}
              onChange={(e) => setComment(e.target.value)}
            />
            <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between" }}>
              <div style={{ display: "flex", gap: 1 }}>
                {[1, 2, 3, 4, 5].map((s) => (
                  <span
                    key={s}
                    onClick={() => setRating(s)}
                    style={{ cursor: "pointer", fontSize: 16, color: s <= rating ? T.yellow : T.border }}
                  >
                    ★
                  </span>
                ))}
              </div>
              <button
                type="submit"
                style={{
                  padding: "5px 14px", borderRadius: 5, border: "none",
                  background: T.accent1, color: "#fff", fontWeight: 600,
                  fontSize: 12, fontFamily: sans, cursor: "pointer",
                }}
              >
                Absenden
              </button>
            </div>
          </form>

          {/* ── History ────────────────────────── */}
          {feedback.length > 0 && (
            <div style={{ display: "flex", flexDirection: "column", gap: 6 }}>
              {feedback.map((f) => (
                <div
                  key={f.id}
                  style={{
                    padding: "8px 10px",
                    background: f.status === "resolved" ? T.green + "06" : T.surface2,
                    borderRadius: 6,
                    border: `1px solid ${f.status === "resolved" ? T.green + "22" : T.border}`,
                  }}
                >
                  <div style={{ display: "flex", alignItems: "center", gap: 6, marginBottom: 3 }}>
                    <span style={{ fontWeight: 600, fontSize: 11, fontFamily: sans }}>{f.author}</span>
                    <span style={{ fontSize: 10, color: T.textDim, fontFamily: mono }}>R{f.round}</span>
                    <span style={{ fontSize: 11, color: T.yellow }}>
                      {"★".repeat(f.rating)}
                    </span>
                    <span style={{ flex: 1 }} />
                    <button
                      onClick={() => handleToggle(f.id)}
                      style={{
                        padding: "1px 6px", borderRadius: 3, border: "none",
                        background: f.status === "resolved" ? T.green + "15" : T.surface2,
                        color: f.status === "resolved" ? T.green : T.textMuted,
                        fontSize: 11, cursor: "pointer",
                      }}
                    >
                      {f.status === "resolved" ? "✅" : "🔲"}
                    </button>
                  </div>
                  <div style={{ fontSize: 12, color: T.text, lineHeight: 1.4 }}>{f.comment}</div>
                </div>
              ))}
            </div>
          )}
        </div>
      )}
    </div>
  );
}
