import os
import json
import time
import pandas as pd
from datetime import datetime
import threading
class QuizApp:
    QUESTIONS_DIR = "questions"
    DATA_DIR = "data"
    CATEGORIES = {
        "1": ("General Knowledge", "general_knowledge.json"),
        "2": ("Science", "science.json"),
        "3": ("History", "history.json"),
    }
    POINTS = {"easy": 10, "medium": 20, "hard": 30}
    DEFAULT_QUESTIONS = 5
    TIMER_SECONDS = 15
    def __init__(self):
        os.makedirs(self.DATA_DIR, exist_ok=True)
        self.leaderboard_path = os.path.join(self.DATA_DIR, "leaderboard.csv")
        self.users_path = os.path.join(self.DATA_DIR, "users.csv")
        self.init_files()
        
    def init_files(self):
        if not os.path.exists(self.leaderboard_path):
            pd.DataFrame(columns=["username", "score", "category", "timestamp"]).to_csv(
                self.leaderboard_path, index=False
            )
        if not os.path.exists(self.users_path):
            pd.DataFrame(
                columns=["username", "attempts", "total_score", "best_score", "best_category"]
            ).to_csv(self.users_path, index=False)

    def load_leaderboard(self):
        return pd.read_csv(self.leaderboard_path)

    def save_leaderboard(self, df):
        df.to_csv(self.leaderboard_path, index=False)

    def load_users(self):
        return pd.read_csv(self.users_path)

    def save_users(self, df):
        df.to_csv(self.users_path, index=False)
    
    def bubble_sort_scores(self, records):
        n = len(records)
        for i in range(n):
            for j in range(0, n - i - 1):
                if records[j]["score"] < records[j + 1]["score"]:
                    records[j], records[j + 1] = records[j + 1], records[j]
                elif records[j]["score"] == records[j + 1]["score"]:
                    if records[j]["timestamp"] < records[j + 1]["timestamp"]:
                        records[j], records[j + 1] = records[j + 1], records[j]
        return records
    def timed_input(self, prompt, timeout):
        answer = [None]
        def get_input():
            answer[0] = input(prompt)
        thread = threading.Thread(target=get_input)
        thread.daemon = True
        thread.start()
        thread.join(timeout)
        if thread.is_alive():
            return None
        return answer[0]

    def load_questions(self, category_file):
        path = os.path.join(self.QUESTIONS_DIR, category_file)
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        df = pd.DataFrame(data)
        df["difficulty"] = df["difficulty"].astype(str).str.lower()
        df.loc[~df["difficulty"].isin(self.POINTS.keys()), "difficulty"] = "easy"
        return df

    def add_leaderboard(self, username, score, category):
        lb = self.load_leaderboard()
        new_row ={
                "username": username,
                "score": int(score),
                "category": category,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            }
        records = lb.to_dict("records")
        records.append(new_row)
        sorted_records = self.bubble_sort_scores(records)
        sorted_records = sorted_records[:10]
        new_df = pd.DataFrame(sorted_records)
        self.save_leaderboard(new_df)

    def show_leaderboard(self):
        lb = self.load_leaderboard()
        if lb.empty:
            print("\nNo scores yet")
            return
        print("\nTop 10 Leaderboard")
        print(lb.head(10).to_string(index=False))

    def update_user(self, username, score, category):
        users = self.load_users()
        if not users.empty:
            users["attempts"] = pd.to_numeric(users["attempts"], errors="coerce").fillna(0).astype(int)
            users["total_score"] = pd.to_numeric(users["total_score"], errors="coerce").fillna(0).astype(int)
            users["best_score"] = pd.to_numeric(users["best_score"], errors="coerce").fillna(0).astype(int)
        score = int(score)
        if users.empty or not (users["username"] == username).any():
            users = pd.concat(
                [users, pd.DataFrame([{
                    "username": username,
                    "attempts": 1,
                    "total_score": score,
                    "best_score": score,
                    "best_category": category
                }])],
                ignore_index=True,
            )
        else:
            m = users["username"] == username
            users.loc[m, "attempts"] += 1
            users.loc[m, "total_score"] += score
            old_best = users.loc[m, "best_score"].iloc[0]
            if score > old_best:
                users.loc[m, "best_score"] = score
                users.loc[m, "best_category"] = category
        self.save_users(users)

    def show_user_stats(self, username):
        users = self.load_users()
        if users.empty or not (users["username"] == username).any():
            print("No stats yet")
            return
        r = users[users["username"] == username].iloc[0]
        attempts = int(r["attempts"]) if int(r["attempts"]) else 0
        total = int(r["total_score"]) if attempts else 0
        best = int(r["best_score"]) if attempts else 0
        best_cat = r.get("best_category", "")
        avg = (total / attempts) if attempts else 0
        print(f"\nStats for {username}")
        print("Attempts:", attempts)
        print("Average:", round(avg, 2))
        print("Best Score:", best)
        if isinstance(best_cat, str) and best_cat.strip():
            print("Best Category:", best_cat)

    def choose_category(self):
        print("Choose category")
        print("\n1. General Knowledge\n2. Science\n3. History")
        c = input("Enter: ").strip()
        if c not in self.CATEGORIES:
            print("Invalid")
            return 
        return self.CATEGORIES[c]

    def ask_timer(self):
        return input(f"Do you want {self.TIMER_SECONDS} secs timer? (yes/no) ").strip().lower() == "yes"

    def run_quiz(self, username):
        picked = self.choose_category()
        if not picked:
            return
        catname, filename = picked
        df = self.load_questions(filename)
        if df.empty:
            print("No questions found")
            return
        n = min(self.DEFAULT_QUESTIONS, len(df))
        timer_on = self.ask_timer()
        chosen = df.sample(n=n).reset_index(drop=True)
        score = 0
        correct = 0
        print(f"\n{catname} Quiz Started\n")
        for i, row in chosen.iterrows():
            diff = str(row.get("difficulty", "easy")).lower()
            pts = self.POINTS.get(diff, 10)
            print(f"Q{i+1}) ({diff.upper()} - {pts} pts) {row['question']}")
            for idx, opt in enumerate(row["options"], start=1):
                print(f"{idx}. {opt}")
            if timer_on:
                ans = self.timed_input("Answer: ", self.TIMER_SECONDS)
                if ans is None:
                    print("Time's up!\n")
                    continue
            else:
                ans = input("Answer: ")
            ans = ans.strip()
            picked_idx = int(ans) - 1 if ans.isdigit() else -1
            right = int(row["answer_index"])
            if picked_idx == right:
                score += pts
                correct += 1
                print("Correct\n")
            else:
                print("Wrong, Correct Option:", row["options"][right], "\n")
        print(f"Finished! Score: {score} | Correct: {correct}\n")
        self.add_leaderboard(username, score, catname)
        self.update_user(username, score, catname)

    def menu(self):
        username = input("Enter Username: ").strip() or "Player"
        while True:
            print("\n1. Start quiz")
            print("2. View leaderboard")
            print("3. View stats")
            print("4. Exit")
            choice = input("Choose option: ").strip()
            if not choice.isdigit():
                print("Invalid Option")
                continue
            ch = int(choice)
            if ch == 1:
                self.run_quiz(username)
            elif ch == 2:
                self.show_leaderboard()
            elif ch == 3:
                self.show_user_stats(username)
            elif ch == 4:
                print("Bye")
                break
            else:
                print("Invalid Option")

if __name__ == "__main__":
    app = QuizApp()
    app.menu()