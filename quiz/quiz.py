import os, json, time
import pandas as pd
from datetime import datetime

QUESTIONS_DIR = "questions"
DATA_DIR = "data"

CATEGORY_FILES = {
    "1": ("General Knowledge", "general_knowledge.json"),
    "2": ("Science", "science.json"),
    "3": ("History", "history.json"),
}

POINTS = {"easy": 10, "medium": 20, "hard": 30}

LEADERBOARD = os.path.join(DATA_DIR, "leaderboard.csv")
USERS = os.path.join(DATA_DIR, "users.csv")

def setup():
    os.makedirs(QUESTIONS_DIR, exist_ok=True)
    os.makedirs(DATA_DIR, exist_ok=True)

    if not os.path.exists(LEADERBOARD):
        pd.DataFrame(columns=["username", "score", "category", "time"]).to_csv(LEADERBOARD, index=False)

    if not os.path.exists(USERS):
        pd.DataFrame(columns=["username", "attempts", "total_score", "best_score"]).to_csv(USERS, index=False)


def load_questions(category_file: str) -> pd.DataFrame:
    path = os.path.join(QUESTIONS_DIR, category_file)
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    df = pd.DataFrame(data)

    df["difficulty"] = df["difficulty"].astype(str).str.lower()
    df.loc[~df["difficulty"].isin(POINTS.keys()), "difficulty"] = "easy"

    return df

def add_to_leaderboard(username: str, score: int, category: str):
    lb = pd.read_csv(LEADERBOARD)
    new = pd.DataFrame([{
        "username": username,
        "score": int(score),
        "category": category,
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }])
    lb = pd.concat([lb, new], ignore_index=True)
    lb = lb.sort_values(["score", "time"], ascending=[False, False]).head(10)
    lb.to_csv(LEADERBOARD, index=False)


def show_leaderboard():
    lb = pd.read_csv(LEADERBOARD)
    if lb.empty:
        print("\nNo scores yet.")
        return
    print("\nTop 10 Leaderboard")
    print(lb.to_string(index=False))

def update_user(username: str, score: int):
    users = pd.read_csv(USERS)

    if users.empty or not (users["username"] == username).any():
        users = pd.concat([users, pd.DataFrame([{
            "username": username,
            "attempts": 1,
            "total_score": int(score),
            "best_score": int(score),
        }])], ignore_index=True)
    else:
        m = users["username"] == username
        users.loc[m, "attempts"] += 1
        users.loc[m, "total_score"] += int(score)
        users.loc[m, "best_score"] = users.loc[m, "best_score"].clip(lower=int(score))

    users.to_csv(USERS, index=False)


def show_user(username: str):
    users = pd.read_csv(USERS)
    if users.empty or not (users["username"] == username).any():
        print("\nNo stats yet.")
        return
    r = users[users["username"] == username].iloc[0]
    avg = r["total_score"] / r["attempts"] if r["attempts"] else 0
    print(f"\nStats for {username}")
    print(f"Attempts: {int(r['attempts'])}")
    print(f"Average : {avg:.2f}")
    print(f"Best    : {int(r['best_score'])}")

def run_quiz(username: str):
    print("\nChoose Category:")
    print("1) General Knowledge\n2) Science\n3) History")
    c = input("Enter: ").strip()
    if c not in CATEGORY_FILES:
        print("Invalid category.")
        return

    category_name, filename = CATEGORY_FILES[c]
    df = load_questions(filename)
    if df.empty:
        print("No questions found.")
        return

    n_raw = input(f"How many questions? (1-{len(df)}) [default 5]: ").strip()
    n = int(n_raw) if n_raw.isdigit() else 5
    n = max(1, min(n, len(df)))

    timer_on = input("Soft timer 15s? (y/N): ").strip().lower() == "y"

    chosen = df.sample(n=n).reset_index(drop=True)

    score = 0
    correct = 0

    print(f"\n{category_name} Quiz Started!\n")

    for i, row in chosen.iterrows():
        diff = row["difficulty"]
        pts = POINTS.get(diff, 10)

        print(f"Q{i+1}) ({diff.upper()} - {pts} pts) {row['question']}")
        for idx, opt in enumerate(row["options"], start=1):
            print(f"  {idx}. {opt}")

        start = time.time()
        ans = input("Answer: ").strip()
        taken = time.time() - start

        timed_out = timer_on and taken > 15

        picked = int(ans) - 1 if ans.isdigit() else -1
        right = int(row["answer_index"])

        if not timed_out and picked == right:
            score += pts
            correct += 1
            print(" Correct!\n")
        else:
            if timed_out:
                print(f"Time up! ({taken:.1f}s)\n")
            print("Wrong. Correct:", row["options"][right], "\n")

    print(f" Finished! Score: {score} | Correct: {correct}/{n}")

    add_to_leaderboard(username, score, category_name)
    update_user(username, score)

def main():
    setup()
    username = input("Enter username: ").strip() or "Player"

    while True:
        print("\nMenu:")
        print("1) Start Quiz")
        print("2) Leaderboard")
        print("3) My Stats")
        print("4) Exit")

        ch = input("Choose: ").strip()

        if ch == "1":
            run_quiz(username)
        elif ch == "2":
            show_leaderboard()
        elif ch == "3":
            show_user(username)
        elif ch == "4":
            print("Bye!")
            break
        else:
            print("Invalid option.")


if __name__ == "__main__":
    main()
