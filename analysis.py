import pandas as pd
from scipy import stats

def categorical_encoding_and_analysis(df, cat_cols):
    summary = {}
    coll=[]
    for c in cat_cols:
        if c in df.columns:
            summary[c] = df[c].value_counts().head(10).to_dict()
            coll.append(c)
    encoded = pd.get_dummies(df, columns=coll, drop_first=True)
    return encoded, summary

def crosstab_and_pivots(df):
    results = {}
    if "region" in df.columns and "final_score" in df.columns:
        temp = df.copy()
        temp["pass"]="Fail"
        temp.loc[temp["final_score"]>=50, "pass"] = "Pass"
        results["crosstab_region_passfail"] = pd.crosstab(temp["region"], temp["pass"], normalize="index").round(3)
    if "gender" in df.columns and "final_score" in df.columns:
        results["pivot_gender_mean_score"] = (df.pivot_table(index="gender", values="final_score", aggfunc="mean").sort_values("final_score", ascending=False)).round(3)
    if "region" in df.columns and "final_score" in df.columns:
        results["pivot_region_mean_score"] = (df.pivot_table(index="region", values="final_score", aggfunc="mean").sort_values("final_score", ascending=False)).round(3)
    return results

def hypothesis_study_hours(df):
    if "study_hours" not in df.columns or "final_score" not in df.columns:
        print("error, study_hours/final_score missing")
        return {"error"}

    x = pd.to_numeric(df["study_hours"], errors="coerce")
    y = pd.to_numeric(df["final_score"], errors="coerce")
    m = df[["study_hours", "final_score"]].dropna()
    x, y = m["study_hours"], m["final_score"]
    if len(x) < 10 or len(y) < 10:
        print("not enough data, data < 10")
        return {"error"}
    r, cor = stats.pearsonr(x, y)
    med = x.median()
    low, high = [], []
    for i in range(len(y)):
        if x.iloc[i]<med:
            low.append(y[i])
        else:
            high.append(y[i])
    low, high = pd.Series(low), pd.Series(high)
    t_stat, p = stats.ttest_ind(high, low, equal_var=False)
    if cor < 0.05:
        corsig="Significant"
    else:
        corsig="Not Significant"
    if p < 0.05:
        diffsig="Significant"
    else:
        diffsig="Not Significant"
    return {
        "n": int(len(x)),
        "pearson_correlation_coefficient": float(r),
        "pearson_probability": float(cor),
        "median_hours_split": float(med),
        "mean_score_low_hours": float(low.mean()),
        "mean_score_high_hours": float(high.mean()),
        "test_statistics": float(t_stat),
        "test_probability": float(p),
        "interpretation": (
            f"Correlation(study hours related to scores) {corsig} (probability value={float(cor):.5f}). "
            f"Group difference(difference between low and high study hours) {diffsig} (probability value={float(p):.5f})."
        )
    }

def actionable_conclusions(df, hypothesis):
    kp = []
    if "attendance_rate" in df.columns and "final_score" in df.columns:
        low, high = [], []
        for i in range(len(df["attendance_rate"])):
            if df["attendance_rate"].iloc[i]<0.7:
                low.append(df["final_score"].iloc[i])
            else:
                high.append(df["final_score"].iloc[i])
        if len(low)>0:
            low = sum(low)/len(low)
        else:
            low = 0
        if len(high)>0:
            high = sum(high)/len(high)
        else:
            high = 0

        kp.append(f"Attendance to Score Relationship: Attendance below 70% average score {float(low):.2f}, Attendance above 70% average score {float(high):.2f}.")
        if high - low > 10:
            kp.append("More Attendance = More Score, send your child to school")
        else:
            kp.append("Happily take leave")
    if "error" not in hypothesis:
        kp.append(hypothesis["interpretation"])
    if not kp:
        kp.append("No data.")
    return kp