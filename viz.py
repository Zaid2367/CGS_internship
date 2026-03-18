import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def save_hist(df, col, fig_dir, filename):
    if col not in df.columns:
        return None
    plt.figure(figsize=(8, 4))
    plt.hist(df[col], bins=20)
    plt.title(f"Histogram: {col}")
    plt.xlabel(col)
    plt.ylabel("Count")
    path = os.path.join(fig_dir, filename)
    plt.tight_layout()
    plt.savefig(path, dpi=180)
    plt.close()
    return path

def save_box(df, vc, gc, fig_dir, filename):
    if vc not in df.columns or gc not in df.columns:
        return None
    groups, labels = [], []
    for k, g in df.groupby(gc):
        groups.append(pd.to_numeric(g[vc], errors="coerce").dropna().values)
        labels.append(str(k))
    if not groups:
        return None
    plt.figure(figsize=(9, 4))
    plt.boxplot(groups, labels=labels, showfliers=True)
    plt.title(f"Boxplot: {vc} by {gc}")
    plt.xlabel(gc)
    plt.ylabel(vc)
    path = os.path.join(fig_dir, filename)
    plt.tight_layout()
    plt.savefig(path, dpi=180)
    plt.close()
    return path

def save_scatter_trend(df, x_col, y_col, fig_dir, filename):
    if x_col not in df.columns or y_col not in df.columns:
        return None
    m = df[[x_col, y_col]].dropna()
    x, y = m[x_col], m[y_col]
    x = pd.to_numeric(x, errors="coerce")
    y = pd.to_numeric(y, errors="coerce")
    if len(x) < 2:
        return None
    plt.figure(figsize=(7, 5))
    plt.scatter(x, y)
    a, b = np.polyfit(x, y, 1)
    xs = np.linspace(x.min(), x.max(), 50)
    plt.plot(xs, a * xs + b)
    plt.title(f"Scatter: {y_col} vs {x_col} (trend)")
    plt.xlabel(x_col)
    plt.ylabel(y_col)
    path = os.path.join(fig_dir, filename)
    plt.tight_layout()
    plt.savefig(path, dpi=180)
    plt.close()
    return path

def save_grouped_bar_mean(df, gc, vc, fig_dir, filename):
    if gc not in df.columns or vc not in df.columns:
        return None
    g = df.groupby(gc)[vc].mean().sort_values(ascending=False)
    plt.figure(figsize=(9, 4))
    plt.bar(g.index.astype(str), g.values)
    plt.title(f"Mean {vc} by {gc}")
    plt.xlabel(gc)
    plt.ylabel(f"Mean {vc}")
    path = os.path.join(fig_dir, filename)
    plt.tight_layout()
    plt.savefig(path, dpi=180)
    plt.close()
    return path