/**
 * Google Apps Script — Dashboard Feedback API
 * =============================================
 * Paste this into your Google Sheet:
 *   Extensions → Apps Script → replace Code.gs content → Save
 *
 * Then deploy:
 *   Deploy → New deployment → Web app
 *   Execute as: Me
 *   Who has access: Anyone
 *   → Copy the URL
 *
 * Sheet must have a tab named "feedback" with header row:
 *   A: id | B: page_id | C: element_id | D: round | E: author
 *   F: comment | G: rating | H: status | I: created_at | J: source
 */

const SHEET_NAME = "feedback";

// ── GET: Read all feedback as JSON ──────────────────────────

function doGet(e) {
  try {
    var sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(SHEET_NAME);
    var data = sheet.getDataRange().getValues();
    var headers = data[0];
    var rows = [];

    for (var i = 1; i < data.length; i++) {
      if (!data[i][0]) continue; // skip empty rows
      var row = {};
      for (var j = 0; j < headers.length; j++) {
        row[headers[j]] = data[i][j];
      }
      // Ensure types
      row.round = Number(row.round);
      row.rating = Number(row.rating);
      row.id = String(row.id);
      rows.push(row);
    }

    return ContentService
      .createTextOutput(JSON.stringify({ status: "ok", data: rows }))
      .setMimeType(ContentService.MimeType.JSON);
  } catch (err) {
    return ContentService
      .createTextOutput(JSON.stringify({ status: "error", message: err.toString() }))
      .setMimeType(ContentService.MimeType.JSON);
  }
}

// ── POST: Add feedback or update status ─────────────────────

function doPost(e) {
  try {
    var payload = JSON.parse(e.postData.contents);
    var sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(SHEET_NAME);

    // ── Action: update_status ─────────────────────────────
    if (payload.action === "update_status") {
      var data = sheet.getDataRange().getValues();
      for (var i = 1; i < data.length; i++) {
        if (String(data[i][0]) === String(payload.id)) {
          sheet.getRange(i + 1, 8).setValue(payload.status); // column H = status
          return ContentService
            .createTextOutput(JSON.stringify({ status: "ok", updated: payload.id }))
            .setMimeType(ContentService.MimeType.JSON);
        }
      }
      return ContentService
        .createTextOutput(JSON.stringify({ status: "error", message: "ID not found" }))
        .setMimeType(ContentService.MimeType.JSON);
    }

    // ── Action: add_feedback (default) ────────────────────
    var id = payload.id || (Date.now().toString(36) + Math.random().toString(36).slice(2, 7));
    var row = [
      id,
      payload.page_id || "",
      payload.element_id || "",
      Number(payload.round) || 1,
      payload.author || "",
      payload.comment || "",
      Number(payload.rating) || 3,
      payload.status || "open",
      payload.created_at || new Date().toISOString(),
      payload.source || "react"
    ];

    sheet.appendRow(row);

    return ContentService
      .createTextOutput(JSON.stringify({ status: "ok", id: id }))
      .setMimeType(ContentService.MimeType.JSON);
  } catch (err) {
    return ContentService
      .createTextOutput(JSON.stringify({ status: "error", message: err.toString() }))
      .setMimeType(ContentService.MimeType.JSON);
  }
}
