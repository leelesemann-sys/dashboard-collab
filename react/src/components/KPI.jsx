import { T, mono, sans } from "../theme";

export default function KPI({ label, value, sub, trend, alert }) {
  return (
    <div
      style={{
        flex: 1,
        minWidth: 150,
        background: T.surface,
        border: `1.5px solid ${alert ? T[alert] + "66" : T.border}`,
        borderRadius: 10,
        padding: "14px 16px",
      }}
    >
      <div style={{ fontSize: 11, fontWeight: 600, color: T.textMuted, textTransform: "uppercase", letterSpacing: 0.5, fontFamily: sans }}>
        {label}
      </div>
      <div style={{ fontSize: 26, fontWeight: 700, fontFamily: mono, color: T.text, marginTop: 4 }}>
        {value}
      </div>
      {sub && (
        <div style={{ fontSize: 12, color: T.textMuted, fontFamily: mono, marginTop: 2 }}>
          {sub}
        </div>
      )}
      {trend && (
        <div style={{ fontSize: 13, fontWeight: 600, fontFamily: mono, color: trend.c, marginTop: 4 }}>
          {trend.v}
        </div>
      )}
    </div>
  );
}
