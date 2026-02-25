import numpy as np
import pandas as pd
from scipy import stats

def categorical_encoding_and_summary(df, cat_cols):
    summary = {}
    for c in cat_cols:
        if c in df.columns:
            summary[c] = df[c].value_counts().head(10).to_dict()
    encoded = pd.get_dummies(df, columns=[c for c in cat_cols if c in df.columns], drop_first=True)
    return encoded, summary

def crosstab_and_pivots(df):
    results = {}
    if "region" in df.columns and "final_score" in df.columns:
        temp = df.copy()
        temp["pass"] = np.where(temp["final_score"] >= 50, "Pass", "Fail")
        results["crosstab_region_passfail"] = pd.crosstab(temp["region"], temp["pass"], normalize="index").round(3)
    if "gender" in df.columns and "final_score" in df.columns:
        results["pivot_gender_mean_score"] = (
            df.pivot_table(index="gender", values="final_score", aggfunc="mean")
              .sort_values("final_score", ascending=False).round(2)
        )
    if "region" in df.columns and "final_score" in df.columns:
        results["pivot_region_mean_score"] = (
            df.pivot_table(index="region", values="final_score", aggfunc="mean")
              .sort_values("final_score", ascending=False).round(2)
        )
    return results
def crosstab_and_pivots(df):
    results={}
    if "region" in df.columns and "final_score" in df.columns:
        temp=df.copy()
        temp["pass"]=np.where(temp["final_score"]>=50, "Pass", "Fail")
        results["crosstab_region_passfail"]=pd.crosstab(temp["region"], temp["pass"], normalize="index").round(3)
    if "gender" in df.columns and "final_score" in df.columns:
        results["pivot_region_mean_score"]=(df.pivot_table(index="gender", values="final_score", aggfunc="mean").sort_values("final_score", ascending=False).round(2))

def hypothesis_study_hours(df, alpha=0.05):
    if "study_hours" not in df.columns or "final_score" not in df.columns:
        return {"error": "study_hours/final_score missing"}

    x = pd.to_numeric(df["study_hours"], errors="coerce")
    y = pd.to_numeric(df["final_score"], errors="coerce")
    m = x.notna() & y.notna()
    x, y = x[m], y[m]
    if len(x) < 10:
        return {"error": "not enough data", "n": int(len(x))}
    r, p_corr = stats.pearsonr(x, y)
    med = x.median()
    low = y[x < med]
    high = y[x >= med]
    t_stat, p_t = stats.ttest_ind(high, low, equal_var=False)
    return {
        "n": int(len(x)),
        "pearson_r": float(r),
        "pearson_p": float(p_corr),
        "median_hours_split": float(med),
        "mean_score_low_hours": float(low.mean()),
        "mean_score_high_hours": float(high.mean()),
        "t_stat": float(t_stat),
        "t_p": float(p_t),
        "interpretation": (
            f"Correlation {'SIGNIFICANT' if p_corr < alpha else 'NOT significant'} (p={p_corr:.4f}). "
            f"Group difference {'SIGNIFICANT' if p_t < alpha else 'NOT significant'} (p={p_t:.4f})."
        )
    }

def actionable_conclusions(df, hypothesis):
    points = []
    if "attendance_rate" in df.columns and "final_score" in df.columns:
        low = df[df["attendance_rate"] < 0.7]["final_score"].mean()
        high = df[df["attendance_rate"] >= 0.7]["final_score"].mean()
        points.append(
            f"Attendance impact: <70% avg score {low:.2f} vs ≥70% avg score {high:.2f}."
        )
    if isinstance(hypothesis, dict) and "error" not in hypothesis:
        points.append(hypothesis["interpretation"])
        points.append("Recommendation: support low-study/low-attendance students with mentoring.")
    if not points:
        points.append("Not enough columns/data to generate strong conclusions.")
    return points