// ── Configuration ────────────────────────────────────────────
// Set VITE_APPS_SCRIPT_URL in .env.local or Vercel Environment Variables
// to enable Google Sheets sync. Without it, feedback stays in localStorage.
export const APPS_SCRIPT_URL = import.meta.env.VITE_APPS_SCRIPT_URL || "";
