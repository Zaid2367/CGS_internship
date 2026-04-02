import pandas as pd

def load_weather_csv(path):
    df = pd.read_csv(path)
    if "date" not in df.columns:
        raise ValueError("Missing required column: date")
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df = df.dropna(subset=["date"]).sort_values("date").set_index("date")
    print(df)
    for c in ["temperature", "humidity", "rainfall", "wind"]:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce")
    return df
def save_cleaned(df, out_path):
    df.reset_index().to_csv(out_path, index=False)