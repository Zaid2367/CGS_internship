import pandas as pd
import matplotlib.pyplot as plt
file="sales_data.csv"
cols={
    "date":"date",
    "region":"region",
    "product":"product",
    "sales":"sales",
    "cost":"cost"
}
def load_file(path):
    if path.endswith(".csv"):
        return pd.read_csv(path)
    return pd.read_excel(path)
def clean(df):
    df=df.copy()
    df["date"]=pd.to_datetime(df["date"],errors="coerce")
    df["sales"]=pd.to_numeric(df["sales"],errors="coerce")
    df["cost"]=pd.to_numeric(df["cost"],errors="coerce")
    x=[c for c in ["date", "sales"] if c in df.columns]
    if x:
        df=df.dropna(subset=x)
    for i in ["region","product"]:
        if i in df.columns:
            df[i]=df[i].fillna("Unknown").astype(str)
    if "cost" in df.columns:
        df["cost"]=df["cost"].fillna(0)
    if {"sales","cost"}.issubset(df.columns):
        df["profit"]=df["sales"]-df["cost"]
        df["profit_margin"]=df["profit"]/df["cost"]
    if "date" in df.columns:
        df["month"]=df["date"].dt.to_period("M").astype(str)
        monthly_sales=df.groupby("month")["sales"].sum().sort_index()
        mdf=monthly_sales.pct_change().reset_index()
        mdf.columns=["month","growth_rate"]
        df=df.merge(mdf, on="month",how="left")
    return df
def main():
    df=load_file(file)
    df=clean(df)
    print("Summary")
    print(df.select_dtypes("number").describe())

    while True:
        print("1. Check Sales by Region(Text)\n")
        print("2. Check Top 10 Product by Sales\n")
        print("3. Check Sales by Month(Text)\n")
        print("4. Check Top 10 Regions by Sales(Graph)\n")
        print("5. Check Monthly Sales Trend(Graph)\n")
        print("6. Check Profit Margin Distribution(Graph)\n")
        print("7. Check Growth Rate(Graph)\n")
        print("8. Exit\n")
        inp=int(input("Enter Option: "))
        if inp==1:
            if "region" in df.columns and "sales" in df.columns:
                sales_region=df.groupby("region")["sales"].sum().sort_values(ascending=False)
                print("Sales by Region\n",sales_region)
        elif inp==2:
            if "product" in df.columns and "sales" in df.columns:
                sales_product=df.groupby("product")["sales"].sum().sort_values(ascending=False).head(10)
                print("Top 10 products by sales\n",sales_product)
        elif inp==3:
            if "month" in df.columns and "sales" in df.columns:
                sales_month=df.groupby("month")["sales"].sum().sort_index()
                print("Sales by Month\n",sales_month)
        elif inp==4:
            if "region" in df.columns and "sales" in df.columns:
                sales_region.head(10).plot(kind="pie",title="Top 10 Regions by Sales")
                plt.tight_layout()
                plt.show()
        elif inp==5:
            if "month" in df.columns and "sales" in df.columns:
                sales_month.plot(kind="line",marker="o",title="Monthly Sales Trend")
                plt.tight_layout()
                plt.show()
        elif inp==6:
            if "profit_margin" in df.columns:
                df["profit_margin"].dropna().plot(kind="bar",title="Profit Margin Distribution")
                plt.tight_layout()
                plt.show()
        elif inp==7:
            print("Growth Rate\n")
            df["growth_rate"].dropna().plot(kind="hist",bins=20,title="Monthly Growth Rate")
        elif inp==8:
            print("Bye")
            break
        else:
            print("Invalid")
    df.to_csv("sales_cleaned.csv",index=False)
    print("Saved")
if __name__ == "__main__":
    main()