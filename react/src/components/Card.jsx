import { T, sans } from "../theme";

export default function Card({ children, title, sub, flex, style }) {
  return (
    <div
      style={{
        flex: flex || 1,
        background: T.surface,
        border: `1px solid ${T.border}`,
        borderRadius: 10,
        padding: "18px 20px",
        ...style,
      }}
    >
      {title && (
        <div style={{ fontWeight: 600, fontSize: 14, color: T.text, fontFamily: sans, marginBottom: 4 }}>
          {title}
        </div>
      )}
      {sub && (
        <div style={{ fontSize: 12, color: T.textMuted, marginBottom: 12 }}>
          {sub}
        </div>
      )}
      {children}
    </div>
  );
}
