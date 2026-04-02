import pandas as pd

def compute_stats(df):
    n = df.select_dtypes(include="number")
    out = {
        "describe": n.describe(percentiles=[0.05, 0.25, 0.5, 0.75, 0.95]).T,
        "variance": n.var(),
        "correlation": n.corr(),
    }
    return out