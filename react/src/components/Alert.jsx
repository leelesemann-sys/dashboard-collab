import { sans } from "../theme";

export default function Alert({ color, children }) {
  return (
    <div
      style={{
        background: color + "08",
        border: `1px solid ${color}33`,
        borderRadius: 8,
        padding: "12px 16px",
        fontSize: 13,
        fontFamily: sans,
        lineHeight: 1.5,
        marginBottom: 14,
      }}
    >
      {children}
    </div>
  );
}
