// ── Theme & Utilities ─────────────────────────────────────────
// Extracted from launch-dashboard, adapted for dashboard-prototyper

export const T = {
  bg: "#f5f6f8",
  surface: "#ffffff",
  surface2: "#f0f2f5",
  border: "#e2e5ea",
  text: "#1a202c",
  textMuted: "#6b7280",
  textDim: "#9ca3af",
  accent1: "#2563eb",
  accent2: "#0891b2",
  green: "#059669",
  red: "#dc2626",
  yellow: "#d97706",
  grid: "#e5e7eb",
};

export const mono = "'JetBrains Mono', monospace";
export const sans = "'DM Sans', -apple-system, sans-serif";

// ── Formatters ───────────────────────────────────────────────

export const fmt = (n) =>
  n == null
    ? "–"
    : n >= 1e6
    ? (n / 1e6).toFixed(1) + "M"
    : n >= 1e3
    ? (n / 1e3).toFixed(0) + "k"
    : n.toLocaleString("de-DE");

export const fmtE = (n) => "€" + fmt(n);

export const pct = (a, b) => (b ? ((a / b) * 100).toFixed(1) + "%" : "–");

export const dlt = (a, b) => {
  if (!b) return { v: "–", c: T.textMuted };
  const d = ((a - b) / b) * 100;
  return { v: (d >= 0 ? "+" : "") + d.toFixed(1) + "%", c: d >= 0 ? T.green : T.red };
};

export const sM = (m) => {
  const [y, mo] = m.split("-");
  const n = ["", "Jan", "Feb", "Mär", "Apr", "Mai", "Jun", "Jul", "Aug", "Sep", "Okt", "Nov", "Dez"];
  return n[parseInt(mo)] + " " + y.slice(2);
};
