// ── Feedback Store (localStorage) ────────────────────────────
const STORAGE_KEY = "dashboard-prototyper-feedback";

function load() {
  try {
    return JSON.parse(localStorage.getItem(STORAGE_KEY)) || [];
  } catch {
    return [];
  }
}

function save(data) {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(data));
}

const nextId = () => Date.now().toString(36) + Math.random().toString(36).slice(2, 7);

// ── CRUD ─────────────────────────────────────────────────────

export function getFeedback(pageId, round) {
  let data = load();
  if (pageId) data = data.filter((d) => d.page_id === pageId);
  if (round) data = data.filter((d) => d.round === round);
  return data.sort((a, b) => new Date(b.created_at) - new Date(a.created_at));
}

export function addFeedback({ pageId, round, author, comment, rating }) {
  const data = load();
  data.push({
    id: nextId(),
    page_id: pageId,
    round,
    author,
    comment,
    rating,
    status: "open",
    created_at: new Date().toISOString(),
  });
  save(data);
}

export function updateStatus(id, status) {
  const data = load();
  const item = data.find((d) => d.id === id);
  if (item) {
    item.status = status;
    save(data);
  }
}

export function getMaxRound() {
  const data = load();
  if (data.length === 0) return 1;
  return Math.max(...data.map((d) => d.round));
}

export function getAllPageIds() {
  const data = load();
  return [...new Set(data.map((d) => d.page_id))];
}

// ── Export ────────────────────────────────────────────────────

function downloadBlob(content, filename, type) {
  const blob = new Blob([content], { type });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = filename;
  a.click();
  URL.revokeObjectURL(url);
}

export function exportCSV() {
  const rows = load();
  const header = "id,page_id,round,author,comment,rating,status,created_at\n";
  const csv = rows
    .map(
      (r) =>
        `${r.id},${r.page_id},${r.round},"${r.author}","${r.comment.replace(/"/g, '""')}",${r.rating},${r.status},${r.created_at}`
    )
    .join("\n");
  downloadBlob(header + csv, "feedback.csv", "text/csv");
}

export function exportJSON() {
  const rows = load();
  downloadBlob(JSON.stringify(rows, null, 2), "feedback.json", "application/json");
}
