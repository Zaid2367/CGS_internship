import os
from src.config import(output, figures, gradesf, attendancef, demof)
from src.io_utils import load_csv, save_json, save_csv
from src.profiling import profile
from src.cleaning import add_features, clip_outliers_iqr
from src.analysis import (categorical_encoding_and_analysis, crosstab_and_pivots,hypothesis_study_hours, actionable_conclusions)
from src.viz import (save_hist, save_box, save_scatter_trend, save_grouped_bar_mean)
from src.report import write_html_report
from src.to_pdf import to_pdf

def main():
    grades = load_csv(gradesf)
    attendance = load_csv(attendancef)
    demo = load_csv(demof)
    df = grades.merge(attendance, on="student_id", how="left").merge(demo, on="student_id", how="left")
    prof_before = profile(df)
    df = add_features(df)
    df = clip_outliers_iqr(df, cols=["final_score", "study_hours"])
    prof_after = profile(df)
    cat_cols = ["gender", "region", "parent_education"]
    cat_anal = categorical_encoding_and_analysis(df, cat_cols)
    tables = crosstab_and_pivots(df)
    hypothesis = hypothesis_study_hours(df)
    figs = []
    figs.append(save_hist(df, "final_score", figures, "hist_finalscore.png"))
    figs.append(save_hist(df, "attendance_rate", figures, "hist_attendance_rate.png"))
    figs.append(save_box(df, "final_score", "gender", figures, "box_scoregender.png"))
    figs.append(save_scatter_trend(df, "study_hours", "final_score", figures, "scatter_hoursscore.png"))
    figs.append(save_grouped_bar_mean(df, "region", "final_score", figures, "bar_meanscoreregion.png"))

    key_points = actionable_conclusions(df, hypothesis)

    save_csv(df, os.path.join(output, "cleaned_students.csv"))
    save_csv(cat_anal[0], os.path.join(output, "cleaned_encoded.csv"))
    findings = {
        "profile_before": prof_before,
        "profile_after": prof_after,
        "hypothesis": hypothesis,
        "categorical_summary": cat_anal[1],
        "key_points": key_points,
    }
    save_json(findings, os.path.join(output, "findings.json"))

    html_path = write_html_report(output, "Student Performance Analysis Report", prof_after, hypothesis, cat_anal[1], key_points, tables, figs)
    pdf_path = to_pdf()

    print("Output folder:", output)

if __name__ == "__main__":
    main()