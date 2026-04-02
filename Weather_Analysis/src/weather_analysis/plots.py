import pandas as pd
import matplotlib.pyplot as plt

def plot_timeseries(df):
    cols = [c for c in ["temperature", "humidity", "rainfall", "wind"] if c in df.columns]
    if not cols:
        print("No columns found")
        return

    fig, axes = plt.subplots(len(cols), 1, figsize=(12, 3 * len(cols)), sharex=True)
    if len(cols) == 1:
        axes = [axes]
    for ax, col in zip(axes, cols):
        ax.plot(df.index, df[col], label=col)

        for w in [7, 30]:
            rc = f"{col}_{w}-day"
            if rc in df.columns:
                ax.plot(df.index, df[rc], label=f"{col} {w}-day")

        ax.set_title(col.capitalize())
        ax.legend()
        ax.grid(True, alpha=0.3)

    fig.tight_layout()
    return fig

def plot_corr_heatmap(corr):
    cols = corr.columns.tolist()
    data = corr.values
    fig, ax = plt.subplots(figsize=(7, 6))
    ax.imshow(data)
    ax.set_xticks(range(len(cols)))
    ax.set_yticks(range(len(cols)))
    ax.set_xticklabels(cols, rotation=45, ha="right")
    ax.set_yticklabels(cols)
    for i in range(len(cols)):
        for j in range(len(cols)):
            ax.text(j, i, f"{data[i, j]:.2f}", ha="center", va="center", fontsize=9)
    ax.set_title("Correlation heatmap")
    fig.tight_layout()
    return fig

def monthly_heatmap(df, col="temperature"):
    if col not in df.columns:
        print(col, "not found")
        return
    daily = df[col].resample("D").mean().interpolate("time").ffill().bfill()
    temp_df = daily.to_frame(name=col)
    temp_df["year"] = temp_df.index.year
    temp_df["month"] = temp_df.index.month
    pivot = temp_df.pivot_table(index="year", columns="month", values=col, aggfunc="mean").sort_index()
    fig, ax = plt.subplots(figsize=(12, 5))
    ax.imshow(pivot.values)
    ax.set_title(f"Monthly Pattern Heatmap ({col}) mean per month")
    ax.set_yticks(range(len(pivot.index)))
    ax.set_yticklabels(pivot.index)
    ax.set_xticks(range(12))
    ax.set_xticklabels(["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"])
    for i in range(pivot.shape[0]):
        for j in range(pivot.shape[1]):
            val = pivot.iloc[i, j]
            if pd.notna(val):
                ax.text(j, i, f"{val:.1f}", ha="center", va="center", fontsize=8)
    fig.tight_layout()
    return fig

def plot_distribution(df, col="temperature"):
    if col not in df.columns:
        print(col, "not found")
        return
    s = df[col].dropna()
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.hist(s, bins=30)
    ax.set_title(f"Distribution of {col}")
    ax.set_xlabel(col)
    ax.set_ylabel("Count")
    fig.tight_layout()
    return fig

def seasonal_decompose_plot(df, col="temperature", period=7):
    if col not in df.columns:
        print(col, "not found")
        return
    try:
        from statsmodels.tsa.seasonal import seasonal_decompose
    except Exception:
        print("statsmodels not installed. Run: pip install statsmodels")
        return
    s = df[col].resample("D").mean().interpolate("time").ffill().bfill()
    try:
        result = seasonal_decompose(s, model="additive", period=period)
    except Exception as e:
        print("Season decomposition failed:", e)
        return
    fig, axes = plt.subplots(4, 1, figsize=(12, 9), sharex=True)
    axes[0].plot(result.observed.index, result.observed.values)
    axes[0].set_title(f"Observed {col}")
    axes[1].plot(result.trend.index, result.trend.values)
    axes[1].set_title("Trend")
    axes[2].plot(result.seasonal.index, result.seasonal.values)
    axes[2].set_title("Seasonal")
    axes[3].plot(result.resid.index, result.resid.values)
    axes[3].set_title("Residual")
    for ax in axes:
        ax.grid(True, alpha=0.3)

    fig.tight_layout()
    return fig