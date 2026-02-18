"""
Load shared mock data and convert to Pandas DataFrames.
"""
import json
from pathlib import Path
import pandas as pd

_DATA_PATH = Path(__file__).parent.parent.parent / "shared" / "mock-data.json"

def _load():
    with open(_DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

_raw = _load()

df_monthly = pd.DataFrame(_raw["monthly"])
df_regions = pd.DataFrame(_raw["regions"])
df_competitors = pd.DataFrame(_raw["competitors"])
kpis = _raw["kpis"]

# Month labels (German)
MONTH_LABELS = {
    "01": "Jan", "02": "Feb", "03": "Mär", "04": "Apr",
    "05": "Mai", "06": "Jun", "07": "Jul", "08": "Aug",
    "09": "Sep", "10": "Okt", "11": "Nov", "12": "Dez",
}

def short_month(m: str) -> str:
    """Convert '2025-05' to 'Mai 25'."""
    parts = m.split("-")
    return MONTH_LABELS.get(parts[1], parts[1]) + " " + parts[0][2:]
