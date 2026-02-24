import numpy as np
import pandas as pd

def add_features(df):
    df = df.copy()

    if {"days_present", "days_total"}.issubset(df.columns):
        df["attendance_rate"] = (df["days_present"] / df["days_total"]).replace([np.inf, -np.inf], np.nan)

    numeric_cols = [
        "math_score", "english_score", "science_score", "final_score",
        "study_hours", "days_present", "days_total", "attendance_rate", "age"
    ]
    for c in numeric_cols:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce")

    return df

def fill_missing(df):
    df = df.copy()

    num_cols = df.select_dtypes(include=[np.number]).columns
    for c in num_cols:
        df[c] = df[c].fillna(df[c].median())

    cat_cols = df.select_dtypes(exclude=[np.number]).columns
    for c in cat_cols:
        if df[c].isna().any():
            mode = df[c].mode(dropna=True)
            df[c] = df[c].fillna(mode.iloc[0] if not mode.empty else "Unknown")

    return df

def clip_outliers_iqr(df, cols, factor=1.5):
    df = df.copy()
    for c in cols:
        if c not in df.columns:
            continue
        s = df[c].astype(float)
        q1, q3 = s.quantile(0.25), s.quantile(0.75)
        iqr = q3 - q1
        lo, hi = q1 - factor * iqr, q3 + factor * iqr
        df[c] = s.clip(lo, hi)
    return df