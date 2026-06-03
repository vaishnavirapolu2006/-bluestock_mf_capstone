import requests
import pandas as pd
from pathlib import Path

RAW_DIR = Path(__file__).resolve().parent.parent / "data" / "raw"

# these are the 5 funds we need to fetch
SCHEMES = {
    "SBI Bluechip":        119551,
    "ICICI Bluechip":      120503,
    "Nippon Large Cap":    118632,
    "Axis Bluechip":       119092,
    "Kotak Bluechip":      120841,
}

def fetch_live_nav(scheme_name, scheme_code):
    url = f"https://api.mfapi.in/mf/{scheme_code}"
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    df = pd.DataFrame(data["data"])
    df["scheme_name"] = scheme_name
    df["scheme_code"] = scheme_code
    return df

if __name__ == "__main__":
    all_data = []
    for name, code in SCHEMES.items():
        print(f"Fetching {name}...")
        df = fetch_live_nav(name, code)
        all_data.append(df)
        print(f"✅ Got {len(df)} rows")

    combined = pd.concat(all_data, ignore_index=True)
    combined.to_csv(RAW_DIR / "live_nav_data.csv", index=False)
    print("\n🎉 Live NAV saved to data/raw/live_nav_data.csv")