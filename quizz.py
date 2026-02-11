import os
import json, time
import pandas as pd
from datetime import datetime
QUESTIONS="questions"
DATA="data"
categories={
    "1":("General Knowledge","general_knowledge.json"),
    "2":("Science","science.json"),
    "3":("History","history.json")
}
leaderboard=os.path.join(DATA,"leaderboard.csv")
users=os.path.join(DATA,"users.csv")
points={"easy":10,"medium":20,"hard":30}
default_questions=5
Timer=15
if not os.path.exists(leaderboard):
    pd.DataFrame(columns=["username","score","category","timestamp"]).to_csv(leaderboard, index=False)
if not os.path.exists(users):
    pd.DataFrame(columns=["username","attempts","total_score","best_score","best_category"]).to_csv(users,index=False)
def save_leaderboard(df):
    df.to_csv(leaderboard, index=False)
def save_users(df):
    df.to_csv(users, index=False)
def load_questions(category_file):
    path=os.path.join(QUESTIONS, category_file)
    with open(path,"r",encoding="utf-8") as f:
        data=json.load(f)
    df=pd.DataFrame(data)
    df["difficulty"]=df["difficulty"].astype(str).str.lower()
    df.loc[~df["difficulty"].isin(points.keys()),"difficulty"]="easy"
    return df
def add_leaderboard(uname,score,category):
    al=pd.read_csv(leaderboard)
    new=pd.DataFrame([{
        "username":uname,
        "score":score,
        "category":category,
        "timestamp":datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }])
    al=pd.concat([al,new],ignore_index=True)
    al=al.sort_values(["score","time"],ascending=[False,False]).head(10)
    al.to_csv(leaderboard,index=False)
def show_leaderboard():
    al=pd.read_csv(leaderboard)
    if al.empty:
        print("\nNo scores yet")
        return
    print("\nTop 10 Leaderboard")
    print(al.to_string(index=False))
def update_user(uname,score):
    use=pd.read_csv(users)
    use["attempts"]=pd.to_numeric(use["attempts"],errors="coerce").fillna(0).astype(int)
    use["total_score"]=pd.to_numeric(use["total_score"],errors="coerce").fillna(0).astype(int)
    use["best_score"]=pd.to_numeric(use["best_score"],errors="coerce").fillna(0).astype(int)
    if use.empty or not (use["username"]==uname).any():
        use=pd.concat([use,pd.DataFrame([{
            "username":uname,
            "attempts":1,
            "total_score":int(score),
            "best_score":int(score)
        }])], ignore_index=True)
    else:
        m=use["username"]==uname
        use.loc[m,"attempts"]+=1
        use.loc[m,"total_score"]+=int(score)
        use.loc[m,"best_score"]=use.loc[m,"best_score"].clip(lower=int(score))
    use.to_csv(users,index=False)
def show_user(uname):
    use=pd.read_csv(users)
    if use.empty or not (use["username"]==uname).any():
        print("no stats yet")
        return
    r=use[use["username"]==uname].iloc[0]
    avg= r["total_score"]/r["attempts"] if r["attempts"] else 0
    print("\nStats for",uname)
    print("Attempts",int(r["attempts"]))
    print("Average",avg)
    print("Best Score",int(r["best_score"]))
def run(uname):
    print("Choose category")
    print("\n1. General Knowledge\n2. Science\n3. History")
    c=input("Enter: ").strip()
    if c not in categories:
        print("Invalid")
        return
    catname, filename = categories[c]
    df=load_questions(filename)
    if df.empty:
        print("no questions found")
        return
    n=max(1,min(5,len(df)))
    timeron=input("Do you want 15secs timer? (yes/no) ").strip().lower()=="yes"
    chosen=df.sample(n=n).reset_index(drop=True)
    score=0
    correct=0
    print(catname,"Quiz Started\n")
    for i, row in chosen.iterrows():
        diff=row["difficulty"]
        pts=points.get(diff,10)
        print(f"Q{i+1}) ({diff.upper()} - {pts} pts) {row['question']}")
        for idx, opt in enumerate(row["options"],start=1):
            print(idx,".",opt)
        start=time.time()
        ans=input("Answer: ").strip()
        taken=time.time()-start
        timeout=timeron and taken>15
        picked = int(ans)-1 if ans.isdigit() else -1
        right=int(row["answer_index"])
        if not timeout and picked == right:
            score+=pts
            correct+=1
            print("Correct\n")
        else:
            if timeout:
                print("Time's up")
            print("Wrong, Correct Option:",row["options"][right],"\n")
    print("Finished! Score:",score,"| Correct:",correct,"\n")
    add_leaderboard(uname,score,catname)
    update_user(uname, score)
def main():
    username=input("Enter Username: ").strip() or "Player"
    while True:
        print("1. Start quiz\n")
        print("2. View leaderboard\n")
        print("3. view stats\n")
        print("4. Exit\n")
        ch=int(input("Choose option: "))
        if ch==1:
            run(username)
        elif ch==2:
            show_leaderboard()
        elif ch==3:
            show_user(username)
        elif ch==4:
            print("Bye")
            break
        else:
            print("Invalid Option")
if __name__=="__main__":
    main()



