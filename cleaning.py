import pandas as pd

def add_features(df):
    df=df.copy()
    if {"days_present","days_total"}.issubset(df.columns):
        df["attendance_rate"]=(df["days_present"]/df["days_total"])
    numeric_cols=["math_score","english_score","science_score","final_score","study_hours","days_present","days_total","attendance_rate","age"]
    for c in numeric_cols:
        if c in df.columns:
            df[c]=pd.to_numeric(df[c],errors="coerce")
    return df

def clip_outliers_iqr(df,cols):
    df=df.copy()
    for c in cols:
        if c not in df.columns:
            continue
        s=df[c]
        q1,q2=s.quantile(0.25),s.quantile(0.75)
        iqr=q2-q1
        l,h=q1-1.5*iqr,q2+1.5*iqr
        df[c]=s.clip(l,h)
    return df
