from . import config
from .io import load_weather_csv, save_cleaned
from .cleaning import fill_missing
from .features import add_rolling_averages
from .stats import compute_stats
from .plots import (
    plot_timeseries,
    plot_corr_heatmap,
    monthly_heatmap,
    plot_distribution,
    seasonal_decompose_plot,
)

def run_cli():
    df = load_weather_csv(config.RAW_FILE)
    df = fill_missing(df)
    df = add_rolling_averages(df, windows=tuple(config.ROLL_WINDOWS))
    stat = compute_stats(df)

    while True:
        print("\n1. Summary")
        print("2. Variance")
        print("3. Correlation")
        print("4. Main Timeseries (Graph)")
        print("5. Correlation heatmap (Graph)")
        print("6. Monthly Heatmap Pattern (Graph)")
        print("7. Distribution (Graph)")
        print("8. Seasonal Decomposition (Graph)")
        print("9. Exit")

        choice = input("Choose option: ").strip()
        if not choice.isdigit():
            print("Invalid number")
            continue

        x = int(choice)

        if x == 1:
            print(stat["describe"])
        elif x == 2:
            print(stat["variance"])
        elif x == 3:
            print(stat["correlation"])
        elif x == 4:
            plot_timeseries(df)
        elif x == 5:
            plot_corr_heatmap(stat["correlation"])
        elif x == 6:
            monthly_heatmap(df, col="temperature")
        elif x == 7:
            plot_distribution(df, col="temperature")
        elif x == 8:
            seasonal_decompose_plot(df, col="temperature", period=7)
        elif x == 9:
            break
        else:
            print("Invalid number")

    save_cleaned(df, config.CLEANED_FILE)
    print("Saved:", config.CLEANED_FILE)