// ── Feedback Store (Google Sheets + localStorage fallback) ──
import { APPS_SCRIPT_URL } from "./config.js";

const STORAGE_KEY = "dashboard-prototyper-feedback";

// ── Local storage helpers ───────────────────────────────────

function loadLocal() {
  try {
    return JSON.parse(localStorage.getItem(STORAGE_KEY)) || [];
  } catch {
    return [];
  }
}

function saveLocal(data) {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(data));
}

const nextId = () =>
  Date.now().toString(36) + Math.random().toString(36).slice(2, 7);

// ── Google Sheets sync helpers ──────────────────────────────

let _remoteCache = null;
let _remoteCacheTime = 0;
const CACHE_TTL = 10_000; // 10 seconds

async function fetchRemote() {
  if (!APPS_SCRIPT_URL) return null;
  // Use cache if fresh
  if (_remoteCache && Date.now() - _remoteCacheTime < CACHE_TTL) {
    return _remoteCache;
  }
  try {
    const res = await fetch(APPS_SCRIPT_URL);
    const json = await res.json();
    if (json.status === "ok") {
      _remoteCache = json.data;
      _remoteCacheTime = Date.now();
      // Also update localStorage as backup
      saveLocal(json.data);
      return json.data;
    }
  } catch (err) {
    console.warn("Sheets sync failed (GET), using localStorage:", err);
  }
  return null;
}

async function postRemote(payload) {
  if (!APPS_SCRIPT_URL) return false;
  try {
    const res = await fetch(APPS_SCRIPT_URL, {
      method: "POST",
      body: JSON.stringify(payload),
    });
    const json = await res.json();
    if (json.status === "ok") {
      _remoteCache = null; // invalidate cache
      return true;
    }
  } catch (err) {
    console.warn("Sheets sync failed (POST), saved locally:", err);
  }
  return false;
}

// ── Unified load: prefer remote, fallback to local ──────────

function load() {
  // Synchronous: return local data (remote is fetched async)
  return loadLocal();
}

// ── CRUD ─────────────────────────────────────────────────────

export function getFeedback(pageId, round, elementId) {
  let data = load();
  if (pageId) data = data.filter((d) => d.page_id === pageId);
  if (round) data = data.filter((d) => d.round === round);
  if (elementId !== undefined)
    data = data.filter(
      (d) => (d.element_id || null) === (elementId || null)
    );
  return data.sort(
    (a, b) => new Date(b.created_at) - new Date(a.created_at)
  );
}

export function getElementCount(pageId, elementId) {
  const data = load();
  return data.filter(
    (d) => d.page_id === pageId && d.element_id === elementId
  ).length;
}

export function addFeedback({ pageId, round, author, comment, rating, elementId }) {
  const entry = {
    id: nextId(),
    page_id: pageId,
    element_id: elementId || null,
    round,
    author,
    comment,
    rating,
    status: "open",
    created_at: new Date().toISOString(),
    source: "react",
  };

  // Save locally immediately
  const data = loadLocal();
  data.push(entry);
  saveLocal(data);

  // Sync to Google Sheets in background
  postRemote(entry);
}

export function updateStatus(id, status) {
  // Update locally
  const data = loadLocal();
  const item = data.find((d) => d.id === id);
  if (item) {
    item.status = status;
    saveLocal(data);
  }

  // Sync to Google Sheets in background
  postRemote({ action: "update_status", id, status });
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

export function getAllElementIds() {
  const data = load();
  return [
    ...new Set(data.filter((d) => d.element_id).map((d) => d.element_id)),
  ];
}

// ── Initial sync: fetch remote data on first load ───────────

export async function syncFromRemote() {
  const remoteData = await fetchRemote();
  if (remoteData) {
    saveLocal(remoteData);
    return true;
  }
  return false;
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
  const header =
    "id,page_id,element_id,round,author,comment,rating,status,created_at,source\n";
  const csv = rows
    .map(
      (r) =>
        `${r.id},${r.page_id},${r.element_id || ""},${r.round},"${r.author}","${(r.comment || "").replace(/"/g, '""')}",${r.rating},${r.status},${r.created_at},${r.source || "react"}`
    )
    .join("\n");
  downloadBlob(header + csv, "feedback.csv", "text/csv");
}

export function exportJSON() {
  const rows = load();
  downloadBlob(
    JSON.stringify(rows, null, 2),
    "feedback.json",
    "application/json"
  );
}
