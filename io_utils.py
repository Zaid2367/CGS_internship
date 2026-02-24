import os
import json
import pandas as pd

def ensure_dirs(out_dir, fig_dir):
    os.makedirs(out_dir, exist_ok=True)
    os.makedirs(fig_dir, exist_ok=True)

def load_csv(path):
    df = pd.read_csv(path)
    if "student_id" not in df.columns:
        raise ValueError(f"Missing 'student_id' in {path}")
    df["student_id"] = df["student_id"].astype(str)
    return df

def save_json(obj, path):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=2)

def save_csv(df, path):
    df.to_csv(path, index=False)