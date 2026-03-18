import pandas as pd
from pathlib import Path

def load_csv(path):
    df = pd.read_csv(path)
    if "student_id" not in df.columns:
        raise ValueError(f"'student_id' column missing in {path.name}")
    df["student_id"] = df["student_id"].astype(str)
    return df

def merge_sources(grades, attendance, demographics):
    df = grades.merge(attendance, on="student_id", how="left").merge(demographics, on="student_id", how="left")
    return df