import { T, sans } from "../theme";

export default function RoundSelector({ currentRound, maxRound, onSelect, onAdd }) {
  const rounds = Array.from({ length: maxRound }, (_, i) => i + 1);
  return (
    <div style={{ display: "flex", alignItems: "center", gap: 6 }}>
      {rounds.map((r) => (
        <button
          key={r}
          onClick={() => onSelect(r)}
          style={{
            padding: "6px 14px",
            borderRadius: 6,
            border: `1.5px solid ${r === currentRound ? T.accent1 : T.border}`,
            background: r === currentRound ? T.accent1 + "12" : T.surface,
            color: r === currentRound ? T.accent1 : T.textMuted,
            fontWeight: r === currentRound ? 700 : 500,
            fontSize: 13,
            fontFamily: sans,
            cursor: "pointer",
            transition: "all 0.15s",
          }}
        >
          Runde {r}
        </button>
      ))}
      <button
        onClick={onAdd}
        style={{
          padding: "6px 10px",
          borderRadius: 6,
          border: `1.5px dashed ${T.border}`,
          background: "transparent",
          color: T.textMuted,
          fontSize: 15,
          fontWeight: 700,
          cursor: "pointer",
          transition: "all 0.15s",
        }}
        title="Neue Runde starten"
      >
        +
      </button>
    </div>
  );
}
