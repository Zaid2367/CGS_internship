import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

file_path="weather.csv"
date_cols=["date","datetime","timestamp","time"]
cols={
    "temperature":["temperature","temp","t"],
    "humidity":["humidity","humid","h"],
    "rainfall":["rainfall","rain","ppt","p"],
    "wind":["wind","windspeed","win","w"]
}
def load(path):
    df=pd.read_csv(path)
    df["date"]=pd.to_datetime(df["date"],errors="coerce")
    df=df.dropna(subset=["date"]).sort_values("date").set_index("date")
    for i in ["temperature","humidity","rainfall","wind"]:
        for i in df.columns:
            df[i]=pd.to_numeric(df[i],errors="coerce")
    return df
def fill_missing(df):
    df=df.copy()
    for i in ["temperature","humidity","wind"]:
        if i in df.columns:
            df[i]=df[i].interpolate(method="time")
            df[i]=df[i].ffill().bfill()
        if "rainfall" in df.columns:
            df["rainfall"]=df["rainfall"].fillna(0)
    return df
def avg(df):
    df=df.copy()
    for i in ["temperature","humidity","rainfall","wind"]:
        if i in df.columns:
            df[f"{i}_7-day"]=df[i].rolling(7,min_periods=1).mean()
            df[f"{i}_30-day"]=df[i].rolling(30,min_periods=1).mean()
    return df
def stats(df):
    n=df.select_dtypes(include="number")
    out={}
    out["describe"]=n.describe(percentiles=[0.05,0.25,0.5,0.75,0.95]).T
    out["variance"]=n.var(numeric_only=True)
    out["correlation"]=n.corr()
    return out
def seasonal(series,period=365):
    try:
        from statsmodels.tsa.seasonal import seasonal_decompose
    except:
        return None
    s=series.resample("D").mean()
    s=s.interpolate("time").ffill().bfill()
    try:
        result=seasonal_decompose(s,model="additive",period=7)
        return result
    except Exception as e:
        print("Season decomposition failed",e)
        return None
def plot_timeseries(df):
    colum=[i for i in ["temperature","humidity","rainfall","wind"] if i in df.columns]
    if not colum:
        print("No columns found")
        return
    fig, axes = plt.subplots(len(colum),1,figsize=(12,3*len(colum)),sharex=True)
    if len(colum)==1:
        axes=[axes]
    for ax, col in zip(axes, colum):
        ax.plot(df.index,df[col],label=col)
        if f"{col}_7-day" in df.columns:
            ax.plot(df.index, df[f"{col}_7-day"],label=f"{col} 7-day")
        if f"{col}_30-day" in df.columns:
            ax.plot(df.index, df[f"{col}_30-day"],label=f"{col} 30-day")
        ax.set_title(col.capitalize())
        ax.legend()
        ax.grid(True,alpha=0.3)
    plt.tight_layout()
    plt.show()
def plot_heatmap(corr):
    colm=corr.columns.tolist()
    data=corr.values
    fig, ax = plt.subplots(figsize=(7,6))
    im = ax.imshow(data)
    ax.set_xticks(range(len(colm)))
    ax.set_yticks(range(len(colm)))
    ax.set_xticklabels(colm,rotation=45,ha="right")
    ax.set_yticklabels(colm)
    for i in range(len(colm)):
        for j in range(len(colm)):
            ax.text(j, i, f"{data[i,j]:.2f}", ha="center", va="center", fontsize=9)
    ax.set_title("Correlation heatmap")
    plt.tight_layout()
    plt.show()
def monthly_heatmap(df,col="temperature"):
    if col not in df.columns:
        print(col,"not found")
        return
    daily=df[col].resample("D").mean().interpolate("time").ffill().bfill()
    temp_df=daily.to_frame(name=col)
    temp_df["year"]=temp_df.index.year
    temp_df["month"]=temp_df.index.month
    pivot=temp_df.pivot_table(index="year",columns="month",values=col,aggfunc="mean").sort_index()
    fig, ax = plt.subplots(figsize=(12,5))
    im=ax.imshow(pivot.values)
    ax.set_title(f"Monthly Pattern Heatmap ({col}) mean per month")
    ax.set_yticks(range(len(pivot.index)))
    ax.set_yticklabels(pivot.index)
    ax.set_xticks(range(12))
    ax.set_xticklabels(["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"])
    for i in range(pivot.shape[0]):
        for j in range(pivot.shape[1]):
            val=pivot.iloc[i,j]
            if pd.notna(val):
                ax.text(j, i, f"{val:.1f}", ha="center", va="center", fontsize=8)
    plt.tight_layout()
    plt.show()
def plot_distribution(df,col="temperature"):
    if col not in df.columns:
        print(col,"not found")
        return
    s=df[col].dropna()
    fig,ax=plt.subplots(figsize=(10,4))
    ax.hist(s,bins=30)
    ax.set_title(f"Distribution of {col}")
    ax.set_xlabel(col)
    ax.set_ylabel("Count")
    plt.tight_layout()
    plt.show()
def plot_seasonal(df,col="temperature"):
    if col not in df.columns:
        print(col,"not found")
        return
    result=seasonal(df[col],period=365)
    if result is None:
        return
    fig, axes=plt.subplots(4,1,figsize=(12,9),sharex=True)
    axes[0].plot(result.observed.index,result.observed.values)
    axes[0].set_title(f"Observed {col}")
    axes[1].plot(result.trend.index,result.trend.values)
    axes[1].set_title("Trend")
    axes[2].plot(result.seasonal.index,result.seasonal.values)
    axes[2].set_title("Seasonal")
    axes[3].plot(result.resid.index,result.resid.values)
    axes[3].set_title("Residual")
    for ax in axes:
        ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()
def main():
    df=load(file_path)
    df=fill_missing(df)
    df=avg(df)
    stat=stats(df)
    while True:
        print("1. Summary")
        print("2. Variance")
        print("3. Correlation")
        print("4. Main Timeseries(Graph)")
        print("5. Correlation heatmap(Graph)")
        print("6. Monthly Heatmap Pattern(Graph)")
        print("7. Distribution(Graph)")
        print("8. Seasonal Decomposition(Graph)")
        print("9. Exit")
        x=int(input("Choose option: "))
        if x==1:
            print(stat["describe"])
        elif x==2:
            print(stat["variance"])
        elif x==3:
            print(stat["correlation"])
        elif x==4:
            plot_timeseries(df)
        elif x==5:
            plot_heatmap(stat["correlation"])
        elif x==6:
            monthly_heatmap(df,col="temperature")
        elif x==7:
            plot_distribution(df,col="temperature")
        elif x==8:
            plot_seasonal(df,col="temperature")
        elif x==9:
            break
        else:
            print("Invalid number")
    df.reset_index().to_csv("Weather_cleaned.csv",index=False)
    print("Saved")
if __name__ == "__main__":
    main()