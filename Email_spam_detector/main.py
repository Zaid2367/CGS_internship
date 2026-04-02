import pandas as pd
import numpy as np
import string
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, ConfusionMatrixDisplay
import nltk
from nltk.corpus import stopwords

nltk.download('stopwords')
df = pd.read_csv("spam.csv", encoding="latin-1")
df = df[['label','message']]
def cust(worrds):
    cleaned=[]
    for i in worrds:
        i=i.lower()
        no_punc=""
        for ch in i:
            if ch not in string.punctuation:
                no_punc+=ch
        words=no_punc.split()
        filtered_words=[]
        for w in words:
            if w not in stop_words:
                filtered_words.append(w)
        clean_text=" ".join(filtered_words)
        cleaned.append(clean_text)
    return cleaned
print("First 5 rows:")
print(df.head())
df["label_num"]=df["label"].map({"ham":0, "spam":1})
stop_words=set(stopwords.words('english'))
df["clean_message"]=cust(df["message"])
print("\nCleaned text sample:")
print(df[['message', 'clean_message']].head())
X = df['clean_message']
y = df['label_num']
X_train_t, X_test_t, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
vectorizer=CountVectorizer() #convert text to numbers
X_train=vectorizer.fit_transform(X_train_t) #learn stuff from train data
X_test=vectorizer.transform(X_test_t) #use same stuff learnt from previous fit func and implement in test data
x_vals = np.linspace(-10, 10, 200) #-10 to 10 shows sigmoid changes from 0 to 1, outside this range its flat
sigmoid = 1 / (1 + np.exp(-x_vals)) #takes num and coverts it to value between 0 and 1
plt.figure(figsize=(8, 5))
plt.plot(x_vals, sigmoid)
plt.title("Sigmoid Function")
plt.xlabel("x")
plt.ylabel("sigmoid(x)")
plt.grid(True)
plt.show()
model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train) #maximizes log-likelihood func. adjusts weights to give correct answers higher probabilities and improve predictictions
y_pred = model.predict(X_test)
y_prob = model.predict_proba(X_test)[:, 1] #gives probability of being spam for each email in test, [:, 1] means we want the probability of spam (class 1)
if len(y_prob)>0:
    print("\nSome probability scores:")
    for i in range(5):
        print(f"Email {i+1}: Probability of spam = {y_prob[i]:.4f}")
accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred)
recall = recall_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred)
print("\nEvaluation Metrics:")
print("Accuracy :", accuracy)
print("Precision:", precision)
print("Recall   :", recall)
print("F1-Score :", f1)

cm = confusion_matrix(y_test, y_pred)
disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=['Not Spam', 'Spam'])
disp.plot()
plt.show()
custom_emails = [
    "Congratulations! You have won a free iPhone. Click here now",
    "Hi Zaid, are we meeting tomorrow for the project discussion?",
    "Urgent! Your bank account is blocked. Verify immediately",
    "Please find the attached report for today meeting"
]
custom_cleaned=cust(custom_emails)
custom_X = vectorizer.transform(custom_cleaned)
custom_pred = model.predict(custom_X)
custom_prob = model.predict_proba(custom_X)[:, 1]
print("\nCustom Email Predictions:")
for i in range(len(custom_emails)):
    if custom_pred[i] == 1:
        label = "Spam"
    else:
        label = "Not Spam"
    print(f"Email: {custom_emails[i]}")
    print(f"Prediction: {label}")
    print(f"Spam Probability: {custom_prob[i]:.4f}")