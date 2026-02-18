# Dashboard Collab

Zwei Varianten eines iterativen Dashboard-Prototyping-Tools mit integriertem Feedback-System.
Zum direkten Vergleich: **Streamlit (Python)** vs. **React/Vite (JSX)**.

## Zweck

Wenn cross-funktionale Teams gemeinsam Dashboards entwickeln:

```
Runde 1: Prototyp  ->  Feedback  ->  Anpassen
Runde 2: Prototyp v2  ->  Feedback  ->  Anpassen
...
Final: Konsens  ->  Umsetzung in Power BI
```

## Live-Demos

| Variante | URL |
|---|---|
| **React** | [dashboard-collab.vercel.app](https://dashboard-collab.vercel.app) |
| **Streamlit** | [Streamlit Cloud](https://dashboard-collab.streamlit.app) |

## Architektur

Beide Varianten schreiben in dasselbe **Google Sheet** als zentrale Datenbank.
So sehen alle Tester (10-20 Personen) dasselbe Feedback, egal welche Variante sie nutzen.

```
React (Vercel)                    Google Apps Script         Google Sheet
+----------------+    POST/JSON  +------------------+       +-----------------+
| feedbackStore  |-------------->| doPost(e)        |------>| "feedback" Tab  |
| .js            |               | doGet(e)         |<------| id, page_id,    |
|                |<--------------|                  |       | element_id, ... |
+----------------+   JSON resp.  +------------------+       +-----------------+
                                                                   ^
Streamlit (Cloud)                                                  |
+----------------+    gspread (Service Account)                    |
| feedback_db.py |------------------------------------------------+
+----------------+
```

### Feedback-Flow

1. **Tester** oeffnet React- oder Streamlit-App
2. Gibt Feedback ein (pro Seite oder pro Chart-Element)
3. Klickt "Absenden"
4. Feedback wird **sofort** im Google Sheet gespeichert
5. Alle anderen Tester sehen es beim naechsten Laden
6. Admin kann Feedback in der Uebersicht filtern, Status aendern, exportieren

### Hybrid-Feedback

Feedback kann auf zwei Ebenen abgegeben werden:

- **Seiten-Level**: Allgemeines Feedback zur ganzen Seite (Formular am Seitenende)
- **Element-Level**: Feedback zu einzelnen Charts/Tabellen (Popover-Button am Chart)

Element-IDs: `trx-chart`, `revenue-chart`, `nrx-rrx-chart`, `market-share-chart`, `region-chart`, `region-table`

## Quick Start

### Streamlit-Variante

```bash
cd streamlit
pip install -r requirements.txt
# Secrets konfigurieren (siehe Setup)
streamlit run app.py
```

### React-Variante

```bash
cd react
npm install
# Optional: .env.local mit VITE_APPS_SCRIPT_URL (siehe Setup)
npm run dev
```

## Setup: Google Sheets Backend

### 1. Google Sheet

- Neues Sheet anlegen, Tab umbenennen zu `feedback`
- Header-Zeile (A-J): `id | page_id | element_id | round | author | comment | rating | status | created_at | source`

### 2. Service Account (fuer Streamlit)

- [Google Cloud Console](https://console.cloud.google.com) -> IAM & Admin -> Dienstkonten -> Erstellen
- Google Sheets API aktivieren
- JSON-Key herunterladen
- Service Account Email als Editor im Sheet einladen

### 3. Apps Script (fuer React)

- Im Google Sheet: Erweiterungen -> Apps Script
- Code aus `docs/apps-script.js` einfuegen
- Deploy -> Neue Bereitstellung -> Web-App -> "Ausfuehren als: Ich", Zugriff: "Jeder"
- URL kopieren

### 4. Secrets konfigurieren

**Streamlit (lokal):** `.streamlit/secrets.toml` aus `.streamlit/secrets.toml.example` erstellen

**Streamlit Cloud:** Settings -> Secrets -> TOML-Inhalt einfuegen

**React/Vercel:** Environment Variable `VITE_APPS_SCRIPT_URL` = Apps Script URL

## Vergleich

| Kriterium | Streamlit | React |
|---|---|---|
| **Sprache** | Python | JavaScript/JSX |
| **Charts** | Plotly | Recharts |
| **Feedback-Backend** | Google Sheets (gspread) | Google Sheets (Apps Script) |
| **Neues Chart** | ~5-10 Zeilen | ~30-50 Zeilen |
| **Neuer Filter** | 1 Zeile (`st.slider`) | State + Handler + JSX |
| **Look & Feel** | Premium CSS, nah an React | Pixel-perfekt, volle Kontrolle |
| **Deploy** | Streamlit Cloud | Vercel |

## Features (beide Varianten)

- 3 Dashboard-Seiten: Executive Summary, Markt-Uptake, Regionale Performance
- Hybrid-Feedback: pro Seite + pro Chart-Element (Popover)
- Runden-System (Runde 1, 2, 3...)
- Feedback-Historie mit Status (offen/erledigt)
- Admin-Seite mit Filtern (Runde, Seite, Element, Status) und Export (CSV/Excel)
- Geteilte Mock-Daten (Pharma-Launch: Cardiozan)
- Google Sheets als persistentes, multi-user Backend

## Projektstruktur

```
dashboard-collab/
  shared/mock-data.json           # Geteilte Pharma-Beispieldaten
  docs/apps-script.js             # Google Apps Script Code (fuer React)
  react/                          # React/Vite Variante
    src/App.jsx                   # Haupt-Shell mit Sync
    src/config.js                 # Apps Script URL Config
    src/feedbackStore.js          # Google Sheets + localStorage Fallback
    src/components/               # KPI, Card, FeedbackBubble, ...
    src/pages/                    # 4 Seiten
  streamlit/                      # Streamlit Variante
    app.py                        # Entry mit st.navigation()
    lib/feedback_db.py            # Google Sheets CRUD (gspread)
    lib/feedback_ui.py            # Element- + Seiten-Feedback UI
    lib/theme.py                  # Premium CSS + KPI Cards
    pages/                        # 4 Seiten
    .streamlit/config.toml        # Theme-Farben
    .streamlit/secrets.toml.example  # Secrets-Template
```

## Lizenz

MIT
