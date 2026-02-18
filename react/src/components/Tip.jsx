import { T, sans } from "../theme";

export default function Tip({ active, payload, label }) {
  if (!active || !payload?.length) return null;
  return (
    <div
      style={{
        background: T.surface,
        border: `1px solid ${T.border}`,
        borderRadius: 8,
        padding: "10px 14px",
        fontSize: 12,
        fontFamily: sans,
        boxShadow: "0 2px 8px rgba(0,0,0,0.08)",
      }}
    >
      <div style={{ fontWeight: 600, marginBottom: 4 }}>{label}</div>
      {payload.map((p, i) => (
        <div key={i} style={{ display: "flex", alignItems: "center", gap: 6, marginTop: 3 }}>
          <span style={{ width: 8, height: 8, borderRadius: 4, background: p.color, display: "inline-block" }} />
          <span style={{ color: T.textMuted }}>{p.name}:</span>
          <span style={{ fontWeight: 600 }}>{typeof p.value === "number" ? p.value.toLocaleString("de-DE") : p.value}</span>
        </div>
      ))}
    </div>
  );
}
