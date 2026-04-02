import pandas as pd

def add_rolling_averages(df, windows=(7, 30)):
    df = df.copy()
    cols = [c for c in ["temperature", "humidity", "rainfall", "wind"] if c in df.columns]
    for c in cols:
        for w in windows:
            df[f"{c}_{w}-day"] = df[c].rolling(w, min_periods=1).mean()
    return df