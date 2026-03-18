import pandas as pd
import matplotlib.pyplot as plt

file = "sales_data.csv"
cols = {
    "date": "date",
    "region": "region",
    "product": "product",
    "sales": "sales",
    "cost": "cost"
}

class SalesAnalyzer:
    def __init__(self, filepath):
        self.filepath = filepath
        self.df = None

    def load_file(self):
        if self.filepath.lower().endswith(".csv"):
            return pd.read_csv(self.filepath)
        return pd.read_excel(self.filepath)

    def clean(self, df):
        df = df.copy()
        if cols["date"] in df.columns:
            df[cols["date"]] = pd.to_datetime(df[cols["date"]], errors="coerce")
            df = df.sort_values(cols["date"])
        if cols["sales"] in df.columns:
            df[cols["sales"]] = pd.to_numeric(df[cols["sales"]], errors="coerce")
            df[cols["sales"]] = df[cols["sales"]].interpolate(method="linear")
        if cols["cost"] in df.columns:
            df[cols["cost"]] = pd.to_numeric(df[cols["cost"]], errors="coerce").fillna(0)
        for c in [cols["region"], cols["product"]]:
            if c in df.columns:
                df[c] = df[c].fillna("Unknown").astype(str)
        if {cols["sales"], cols["cost"]}.issubset(df.columns):
            df["profit"] = df[cols["sales"]] - df[cols["cost"]]
            safe_cost = df[cols["cost"]].replace(0, pd.NA)
            df["profit_margin"] = (df["profit"] / safe_cost)
        if cols["date"] in df.columns and cols["sales"] in df.columns:
            df["month"] = df[cols["date"]].dt.to_period("M").astype(str)
            monthly_sales = df.groupby("month")[cols["sales"]].sum().sort_index()
            growth = monthly_sales.pct_change().reset_index()
            growth.columns = ["month", "growth_rate"]
            df = df.merge(growth, on="month", how="left")
        return df

    def show_summary(self):
        if self.df is None:
            return
        print("Summary")
        print(self.df.select_dtypes("number").describe())

    def sales_by_region(self):
        if cols["region"] not in self.df.columns or cols["sales"] not in self.df.columns:
            print("Required columns missing.")
            return None
        result = self.df.groupby(cols["region"])[cols["sales"]].sum().sort_values(ascending=False)
        print("Sales by Region\n", result)
        return result

    def top_products(self):
        if cols["product"] not in self.df.columns or cols["sales"] not in self.df.columns:
            print("Required columns missing.")
            return None
        result = self.df.groupby(cols["product"])[cols["sales"]].sum().sort_values(ascending=False).head(10)
        print("Top 10 products by sales\n", result)
        return result

    def sales_by_month(self):
        if "month" not in self.df.columns or cols["sales"] not in self.df.columns:
            print("Required columns missing.")
            return None
        result = self.df.groupby("month")[cols["sales"]].sum().sort_index()
        print("Sales by Month\n", result)
        return result

    def plot_top_regions(self):
        sales_region = self.sales_by_region()
        if sales_region is None:
            return
        sales_region.head(10).plot(kind="pie", title="Top 10 Regions by Sales")
        plt.tight_layout()
        plt.show()

    def plot_monthly_trend(self):
        sales_month = self.sales_by_month()
        if sales_month is None:
            return
        sales_month.plot(kind="line", marker="o", title="Monthly Sales Trend")
        plt.xlabel("Month")
        plt.ylabel("Total Sales")
        plt.tight_layout()
        plt.show()

    def plot_profit_margin_dist(self):
        if "profit_margin" not in self.df.columns:
            print("profit_margin column missing.")
            return
        self.df["profit_margin"].dropna().plot(kind="hist", bins=20, title="Profit Margin Distribution")
        plt.xlabel("Profit Margin")
        plt.ylabel("Frequency")
        plt.tight_layout()
        plt.show()

    def plot_growth_rate(self):
        if "growth_rate" not in self.df.columns:
            print("growth_rate column missing.")
            return
        self.df["growth_rate"].dropna().plot(kind="hist", bins=20, title="Monthly Growth Rate")
        plt.xlabel("Growth Rate")
        plt.ylabel("Frequency")
        plt.tight_layout()
        plt.show()

    def save_cleaned(self, out_path="sales_cleaned.csv"):
        if self.df is None:
            return
        self.df.to_csv(out_path, index=False)
        print("Saved:", out_path)

    def run(self):
        raw = self.load_file()
        self.df = self.clean(raw)
        self.show_summary()

        while True:
            print("\n1. Check Sales by Region(Text)")
            print("2. Check Top 10 Product by Sales(Text)")
            print("3. Check Sales by Month(Text)")
            print("4. Check Top 10 Regions by Sales(Graph)")
            print("5. Check Monthly Sales Trend(Graph)")
            print("6. Check Profit Margin Distribution(Graph)")
            print("7. Check Growth Rate(Graph)")
            print("8. Exit")

            choice = input("Enter Option: ").strip()
            if not choice.isdigit():
                print("Invalid")
                continue

            inp = int(choice)

            if inp == 1:
                self.sales_by_region()
            elif inp == 2:
                self.top_products()
            elif inp == 3:
                self.sales_by_month()
            elif inp == 4:
                self.plot_top_regions()
            elif inp == 5:
                self.plot_monthly_trend()
            elif inp == 6:
                self.plot_profit_margin_dist()
            elif inp == 7:
                self.plot_growth_rate()
            elif inp == 8:
                print("Bye")
                break
            else:
                print("Invalid")

        self.save_cleaned()

if __name__ == "__main__":
    app = SalesAnalyzer(file)
    app.run()