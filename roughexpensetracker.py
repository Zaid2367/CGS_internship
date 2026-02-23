import os
import pandas as pd
from datetime import date, timedelta, datetime
categories=["Food","Transport","Entertainment","Bills","Shopping","Health","Other"]
columns=["id","date","amount","category","description"]
expensefile="expenses.csv"
categoriesfile="categories.csv"
def save(df):
    out=df.copy()
    out["date"]=pd.to_datetime(out["date"]).dt.strftime("%Y-%m-%d")
    out.to_csv(expensefile, index=False)
def savecat(categories):
    pd.DataFrame({"categories": categories}).to_csv(categoriesfile,index=False)

if not os.path.exists(expensefile):
    df=pd.DataFrame(columns=columns)
    df.to_csv(expensefile,index=False)
if not os.path.exists(categoriesfile):
    df=pd.DataFrame({"categories": categories}).to_csv(categoriesfile,index=False)
df=pd.read_csv(expensefile)
df["date"]=pd.to_datetime(df["date"],errors="coerce").dt.date
df["amount"]=pd.to_numeric(df["amount"],errors="coerce")
catdf = pd.read_csv(categoriesfile)
categories = catdf["categories"].dropna().astype(str).tolist()

while True:
    print("1. Add expense")
    print("2. View expense")
    print("3. Edit expenses")
    print("4. Delete expenses")
    print("5. Category management")
    print("6. Weekly summary")
    print("7. Monthly summary")
    print("8. Custom date range summary")
    print("9. Exit")
    x = int(input("Choose option: "))
    if x==1:
        amt=float(input("Enter Amount: "))
        if amt <=0:
            print("Invalid Amount! Try Again")
            continue
        for i in range(len(categories)):
            print(i,":",categories[i],end="\n")
        cat = int(input("Select the category: "))
        if not (0 <= cat < len(categories)):
            print("Invalid category number")
            continue
        cate=categories[cat]
        date_str=input("Enter date (YYYY-MM-DD): ").strip()
        if date_str == "":
            datee = date.today()
        else:
            d=pd.to_datetime(date_str,errors="coerce")
            if pd.isna(d):
                print("Invalid date, use (YYYY-MM-DD) format")
                continue
            datee=d.date()
        desc=input("Enter the Description: ")
        newrow={
            "id": 1 if df.empty or df['id'].isna().all() else int(df['id'].max())+1,
            "date":datee,
            "amount":amt,
            "category":cate,
            "description":desc
        }
        df=pd.concat([df,pd.DataFrame([newrow])],ignore_index=True)
        save(df)
        print("Added Expense")
    elif x==2:
        print(df)
    elif x==3:
        print(df[['id','amount']])
        aedtd=int(input("Enter id of the amount that needs to be edited: "))
        amtedit=df["id"]==aedtd
        if not amtedit.any():
            print("Invalid id")
            continue
        newamt=float(input("Enter the new Amount: "))
        if newamt <=0:
            print("Invalid Amount! Try Again")
            continue
        df.loc[amtedit,"amount"]=round(newamt,2)
        save(df)
        print("Edited, the new amount for id",aedtd,"is", newamt)
    elif x==4:
        print(df)
        did=int(input("Enter id of the data to delete: "))
        delid=df["id"]==did
        if not delid.any():
            print("Invalid Index! Try Again")
            continue
        df=df.loc[~delid].copy()
        save(df)
        print("Deleted")
    elif x==5:
        print("1. View Category")
        print("2. Add Category")
        print("3. Delete Category")
        print("4. Back")
        catchoose=int(input("Choose the option: "))
        if catchoose==1:
            print(categories)
        elif catchoose==2:
            catpick=input("New category name: ")
            categories.append(catpick)
            savecat(categories)
            print("Added")
        elif catchoose==3:
            print(categories)
            catdel=input("Enter category you want to delete: ")
            if catdel in categories:
                categories.remove(catdel)
            savecat(categories)
            print("Deleted")
        else:
            continue
    elif x==6:
        end=date.today()
        start=end-timedelta(days=6)
        week=df[(df["date"]>=start)&(df["date"]<=end)]
        print(week,"\nWeekly Summary from",start,"to",end)
    elif x==7:
        ym=input("Enter month (YYYY-MM): ").strip()
        try:
            y, m= map(int, ym.split("-"))
            if not 1<=m<=12: 
                print("Invalid") 
                continue 
            start=date(y,m,1) 
            if m==12: 
                end=date(y+1,1,1)-timedelta(days=1) 
            else: 
                end=date(y,m+1,1)-timedelta(days=1) 
                mont=df[(df["date"]>=start)&(df["date"]<=end)] 
                print(mont,"\nMonthly Summary from",start,"to",end)
        except Exception:
            print("Invalid date. Use YYYY-MM-DD")
    elif x == 8:
        try:
            start_input = input("Enter start date (YYYY-MM-DD): ").strip()
            end_input = input("Enter end date (YYYY-MM-DD): ").strip()
            start = datetime.strptime(start_input, "%Y-%m-%d").date()
            end = datetime.strptime(end_input, "%Y-%m-%d").date()
            if start > end:
                print("Start date cannot be after end date")
                continue
            if pd.api.types.is_datetime64_any_dtype(df["date"]):
                m = (df["date"].dt.date >= start) & (df["date"].dt.date <= end)
            else:
                m = (df["date"] >= start) & (df["date"] <= end)
            result = df[m]
            if result.empty:
                print("No data found in this range.")
            else:
                print(result)
                print("\nSummary from", start, "to", end)
        except Exception:
            print("Invalid date format. Use YYYY-MM-DD")

    elif x==9:
        print("Exited")
        break
    else:
        print("invalid number try again")