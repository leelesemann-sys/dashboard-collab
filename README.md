# Dashboard Collab

> **Language:** English | [Deutsch](README.de.md)

Two variants of an iterative dashboard prototyping tool with built-in feedback collection.
Side-by-side comparison: **Streamlit (Python)** vs. **React/Vite (JSX)**.

## Purpose

For cross-functional teams developing dashboards collaboratively:

```
Round 1: Prototype  ->  Feedback  ->  Adjust
Round 2: Prototype v2  ->  Feedback  ->  Adjust
...
Final: Consensus  ->  Build in Power BI
```

## Live Demos

| Variant | URL |
|---|---|
| **React** | [dashboard-collab.vercel.app](https://dashboard-collab.vercel.app) |
| **Streamlit** | [dashboard-collab.streamlit.app](https://dashboard-collab.streamlit.app) |

## Architecture

Both variants write to the same **Google Sheet** as a shared database.
All testers (10-20 people) see the same feedback regardless of which variant they use.

```
React (Vercel)                    Google Apps Script         Google Sheet
+----------------+    POST/JSON  +------------------+       +-----------------+
| feedbackStore  |-------------->| doPost(e)        |------>| "feedback" tab  |
| .js            |               | doGet(e)         |<------| id, page_id,    |
|                |<--------------|                  |       | element_id, ... |
+----------------+   JSON resp.  +------------------+       +-----------------+
                                                                   ^
Streamlit (Cloud)                                                  |
+----------------+    gspread (Service Account)                    |
| feedback_db.py |------------------------------------------------+
+----------------+
```

### Feedback Flow

1. **Tester** opens React or Streamlit app
2. Enters feedback (per page or per chart element)
3. Clicks "Submit"
4. Feedback is **instantly** saved to the Google Sheet
5. All other testers see it on next load
6. Admin can filter, change status, and export feedback

### Hybrid Feedback

Feedback can be submitted at two levels:

- **Page-level**: General feedback for the entire page (form at page bottom)
- **Element-level**: Feedback for individual charts/tables (popover button on each chart)

Element IDs: `trx-chart`, `revenue-chart`, `nrx-rrx-chart`, `market-share-chart`, `region-chart`, `region-table`

## Quick Start

### Streamlit Variant

```bash
cd streamlit
pip install -r requirements.txt
# Configure secrets (see Setup below)
streamlit run app.py
```

### React Variant

```bash
cd react
npm install
# Optional: create .env.local with VITE_APPS_SCRIPT_URL (see Setup below)
npm run dev
```

## Setup: Google Sheets Backend

### 1. Google Sheet

- Create a new Google Sheet, rename the tab to `feedback`
- Header row (A-J): `id | page_id | element_id | round | author | comment | rating | status | created_at | source`

### 2. Service Account (for Streamlit)

- [Google Cloud Console](https://console.cloud.google.com) -> IAM & Admin -> Service Accounts -> Create
- Enable the Google Sheets API
- Download the JSON key
- Invite the service account email as Editor on the Sheet

### 3. Apps Script (for React)

- In Google Sheet: Extensions -> Apps Script
- Paste the code from `docs/apps-script.js`
- Deploy -> New Deployment -> Web App -> "Execute as: Me", Access: "Anyone"
- Copy the URL

### 4. Configure Secrets

**Streamlit (local):** Copy `.streamlit/secrets.toml.example` to `.streamlit/secrets.toml` and fill in values

**Streamlit Cloud:** Settings -> Secrets -> paste the TOML content

**React/Vercel:** Environment Variable `VITE_APPS_SCRIPT_URL` = Apps Script URL

## Comparison

| Criterion | Streamlit | React |
|---|---|---|
| **Language** | Python | JavaScript/JSX |
| **Charts** | Plotly | Recharts |
| **Feedback Backend** | Google Sheets (gspread) | Google Sheets (Apps Script) |
| **New chart** | ~5-10 lines | ~30-50 lines |
| **New filter** | 1 line (`st.slider`) | State + handler + JSX |
| **Look & Feel** | Premium CSS, close to React | Pixel-perfect, full control |
| **Deploy** | Streamlit Cloud | Vercel |

## Features (both variants)

- 3 dashboard pages: Executive Summary, Market Uptake, Regional Performance
- Hybrid feedback: per page + per chart element (popover)
- Round system (Round 1, 2, 3...)
- Feedback history with status (open/resolved)
- Admin page with filters (round, page, element, status) and export (CSV/Excel)
- Shared mock data (pharma launch: Cardiozan)
- Google Sheets as persistent, multi-user backend

## Project Structure

```
dashboard-collab/
  shared/mock-data.json           # Shared pharma mock data
  docs/apps-script.js             # Google Apps Script code (for React)
  react/                          # React/Vite variant
    src/App.jsx                   # Main shell with sync
    src/config.js                 # Apps Script URL config
    src/feedbackStore.js          # Google Sheets + localStorage fallback
    src/components/               # KPI, Card, FeedbackBubble, ...
    src/pages/                    # 4 pages
  streamlit/                      # Streamlit variant
    app.py                        # Entry with st.navigation()
    lib/feedback_db.py            # Google Sheets CRUD (gspread)
    lib/feedback_ui.py            # Element + page feedback UI
    lib/theme.py                  # Premium CSS + KPI cards
    pages/                        # 4 pages
    .streamlit/config.toml        # Theme colors
    .streamlit/secrets.toml.example  # Secrets template
```

## License

MIT
