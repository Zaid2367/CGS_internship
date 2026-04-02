import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.metrics import accuracy_score, precision_score, recall_score, confusion_matrix, ConfusionMatrixDisplay
from sklearn.preprocessing import LabelEncoder

df = pd.read_csv("loan_data_big.csv")
print("First 5 rows:")
print(df.head())
for col in df.columns:
    if df[col].dtype == "object":
        df[col] = df[col].fillna(df[col].mode()[0])
    else:
        df[col] = df[col].fillna(df[col].median())
label_encoders = {}
for col in df.columns:
    if df[col].dtype == "object":
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col])
        label_encoders[col] = le
print("\nData after encoding:")
print(df.head())
X = df.drop("Loan_Status", axis=1)
y = df["Loan_Status"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
shallow_tree = DecisionTreeClassifier(max_depth=3, class_weight="balanced", random_state=42)
shallow_tree.fit(X_train, y_train)
y_pred_shallow = shallow_tree.predict(X_test)
print("\nShallow Tree Results")
print("Accuracy :", accuracy_score(y_test, y_pred_shallow))
print("Precision:", precision_score(y_test, y_pred_shallow))
print("Recall   :", recall_score(y_test, y_pred_shallow))
print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred_shallow))
deep_tree = DecisionTreeClassifier(class_weight="balanced", random_state=42)
deep_tree.fit(X_train, y_train)
y_pred_deep = deep_tree.predict(X_test)
print("\nDeep Tree Results")
print("Accuracy :", accuracy_score(y_test, y_pred_deep))
print("Precision:", precision_score(y_test, y_pred_deep))
print("Recall   :", recall_score(y_test, y_pred_deep))
print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred_deep))
cm = confusion_matrix(y_test, y_pred_shallow)
disp = ConfusionMatrixDisplay(confusion_matrix=cm)
disp.plot()
plt.title("Confusion Matrix - Shallow Tree")
plt.show()
plt.figure(figsize=(14, 7))
plot_tree(shallow_tree, feature_names=X.columns, class_names=["Rejected", "Approved"], filled=True)
plt.title("Decision Tree Visualization (Shallow Tree)")
plt.show()
importances = pd.Series(shallow_tree.feature_importances_, index=X.columns)
importances = importances.sort_values(ascending=False)
plt.figure(figsize=(8, 5))
plt.bar(importances.index, importances.values)
plt.title("Feature Importances")
plt.xlabel("Features")
plt.ylabel("Importance")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()