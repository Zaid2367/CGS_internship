import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.preprocessing import StandardScaler
df=pd.read_csv('house_prices.csv')
print(df.head())
plt.figure(figsize=(6,4))
plt.scatter(df["area"],df["price"])
plt.xlabel("Area")
plt.ylabel("Price")
plt.grid(True)
plt.show()
plt.figure(figsize=(6,4))
plt.scatter(df["rooms"],df["price"])
plt.xlabel("Rooms")
plt.ylabel("Price")
plt.grid(True)
plt.show()

x=df["area"].values
y=df["price"].values
def gradient_descent(mm,bb,dataa,L):
    m_grad=0
    b_grad=0
    n=len(dataa)
    for i in range(n):
        x=dataa.iloc[i]["area"]
        y=dataa.iloc[i]["price"]
        y_pred=mm*x+bb
        m_grad+=-(2/n)*x*(y-y_pred)
        b_grad+=-(2/n)*(y-y_pred)
    m=mm-L*m_grad
    b=bb-L*b_grad
    return m,b
m=0
b=0
lr=0.0000001
epochs=1000
for i in range(epochs):
    if i%100==0:
        print(f"Epoch {i}: m= {m:.4f}, b= {b:.4f}")
    m,b=gradient_descent(m,b,df,lr)
print("from scratch: m=",m," b=",b)

y_line=m*x+b
plt.figure(figsize=(6,4))
plt.scatter(x,y,label="Actual Data")
plt.plot(x,y_line,label="Regression Line")
plt.xlabel("Area")
plt.ylabel("Price")
plt.title("Linear Regression")
plt.legend()
plt.grid(True)
plt.show()

mae_scratch=mean_absolute_error(y,y_line)
mse_scratch=mean_squared_error(y,y_line)
r2_scratch=r2_score(y,y_line)
print("From scratch metrics: \nMAE:",mae_scratch,"\nMSE:",mse_scratch,"\nR2 Score:",r2_scratch)

df_encoded=pd.get_dummies(df,columns=["location"],drop_first=True)
x=df_encoded.drop("price",axis=1).values
y=df_encoded["price"].values
x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.2,random_state=42)
model=LinearRegression()
model.fit(x_train,y_train)
y_pred_test=model.predict(x_test)
#print("skikit learn model: \nIntercept(b):",model.intercept_,"\nCoefficients(m):",model.coef_)

mae=mean_absolute_error(y_test,y_pred_test)
mse=mean_squared_error(y_test,y_pred_test)
r2=r2_score(y_test,y_pred_test)
print("skikit learn Metrics: \nMAE:",mae,"\nMSE:",mse,"\nR2 Score:",r2)
arr=int(input("Enter area of new house: "))
roo=int(input("Enter number of rooms: "))
locc=input("Enter location (A/B/C): ").upper()
new_house=pd.DataFrame({
    "area":[arr],
    "rooms":[roo],
    "location_B":1 if locc=="B" else 0,
    "location_C":1 if locc=="C" else 0
})
new_pred=model.predict(new_house)
print("Predicted price for new house:",new_pred[0])
x_scaled=df_encoded.drop("price",axis=1)
y_scaled=df_encoded["price"]
x_train_s,x_test_s,y_train_s,y_test_s=train_test_split(x_scaled,y_scaled,test_size=0.2,random_state=42)
scaler=StandardScaler()
x_train_scaled=scaler.fit_transform(x_train_s)
x_test_scaled=scaler.transform(x_test_s)
scaled_model=LinearRegression()
scaled_model.fit(x_train_scaled,y_train_s)
y_pred_scaled=scaled_model.predict(x_test_scaled)
mae_scaled=mean_absolute_error(y_test_s,y_pred_scaled)
mse_scaled=mean_squared_error(y_test_s,y_pred_scaled)
r2_scaled=r2_score(y_test_s,y_pred_scaled)
print("Feature Scaling: \nMAE:",mae_scaled,"\nMSE:",mse_scaled,"\nR2 Score:",r2_scaled)