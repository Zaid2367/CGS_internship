import pandas as pd

def fill_missing(df):
    df = df.copy()
    for c in ["temperature", "humidity", "wind"]:
        if c in df.columns:
            df[c] = df[c].interpolate(method="time").ffill().bfill()
    if "rainfall" in df.columns:
        df["rainfall"] = df["rainfall"].fillna(0)
    return df