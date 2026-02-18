# Dashboard Prototyper

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

## Quick Start

### Streamlit-Variante

```bash
cd streamlit
pip install -r requirements.txt
streamlit run app.py
```

### React-Variante

```bash
cd react
npm install
npm run dev
```

## Vergleich

| Kriterium | Streamlit | React |
|---|---|---|
| **Sprache** | Python | JavaScript/JSX |
| **Charts** | Plotly | Recharts |
| **Feedback-Speicher** | SQLite (server-seitig, multi-user) | localStorage (browser-lokal) |
| **Neues Chart** | ~5-10 Zeilen | ~30-50 Zeilen |
| **Neuer Filter** | 1 Zeile (`st.slider`) | State + Handler + JSX |
| **Look & Feel** | Funktional, Standard | Pixel-perfekt, volle Kontrolle |
| **Backend noetig** | Nein (eingebaut) | Ja (fuer Multi-User) |
| **Deploy** | Streamlit Cloud | Vercel / GitHub Pages |

## Features (beide Varianten)

- 3 Dashboard-Seiten: Executive Summary, Markt-Uptake, Regionale Performance
- Feedback-Formular pro Seite (Name, Kommentar, Sterne-Bewertung)
- Runden-System (Runde 1, 2, 3...)
- Feedback-Historie mit Status (offen/erledigt)
- Admin-Seite mit Filtern und Export (CSV/Excel bzw. CSV/JSON)

## Projektstruktur

```
dashboard-prototyper/
  shared/mock-data.json        # Geteilte Pharma-Beispieldaten
  react/                       # React/Vite Variante
    src/App.jsx                # Haupt-Shell
    src/components/            # KPI, Card, FeedbackPanel, ...
    src/pages/                 # 4 Seiten
    src/feedbackStore.js       # localStorage CRUD
  streamlit/                   # Streamlit Variante
    app.py                     # Entry mit st.navigation()
    lib/feedback_db.py         # SQLite CRUD
    pages/                     # 4 Seiten
```
