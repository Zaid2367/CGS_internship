def profile(df):
    return {
        "rows": int(df.shape[0]),
        "cols": int(df.shape[1]),
        "duplicates": int(df.duplicated().sum()),
        "missing_percent": (df.isna().mean() * 100).round(2).to_dict(),
        "dtypes": df.dtypes.astype(str).to_dict(),
    }