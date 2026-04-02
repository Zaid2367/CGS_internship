import streamlit as st
import pandas as pd

from src.weather_analysis.io import load_weather_csv, save_cleaned
from src.weather_analysis.cleaning import fill_missing
from src.weather_analysis.features import add_rolling_averages
from src.weather_analysis.stats import compute_stats
from src.weather_analysis.plots import (
    plot_timeseries,
    plot_corr_heatmap,
    monthly_heatmap,
    plot_distribution,
    seasonal_decompose_plot,
)
st.title("Weather Analysis Dashboard")
uploaded = st.file_uploader("Upload weather.csv", type=["csv"])
if uploaded is None:
    st.stop()

df = pd.read_csv(uploaded)
df["date"] = pd.to_datetime(df["date"], errors="coerce")
df = df.dropna(subset=["date"]).sort_values("date").set_index("date")
df = fill_missing(df)
df = add_rolling_averages(df)
stat = compute_stats(df)

st.subheader("Summary")
st.dataframe(stat["describe"])
st.subheader("Variance")
st.dataframe(stat["variance"])
st.subheader("Correlation")
st.dataframe(stat["correlation"])

st.subheader("Time Series")
fig = plot_timeseries(df)
st.pyplot(fig)

st.subheader("Correlation Heatmap")
fig = plot_corr_heatmap(stat["correlation"])
st.pyplot(fig)

st.subheader("Monthly Heatmap")
fig = monthly_heatmap(df, col="temperature")
st.pyplot(fig)

st.subheader("Distribution")
fig = plot_distribution(df, col="temperature")
st.pyplot(fig)

st.subheader("Seasonal Decomposition")
fig = seasonal_decompose_plot(df, col="temperature", period=7)
st.pyplot(fig)

csv = df.reset_index().to_csv(index=False).encode("utf-8")
st.download_button("Download Cleaned CSV", csv, "Weather_cleaned.csv")