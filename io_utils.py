import os
import json
import pandas as pd

def load_csv(path):
    df = pd.read_csv(path)
    if "student_id" not in df.columns:
        print(f"Missing student Id in {path}")
        return
    df["student_id"] = df["student_id"].astype(str)
    return df
def save_json(obj, path):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f)
def save_csv(df, path):
    df.to_csv(path, index=False)