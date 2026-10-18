import pandas as pd
import numpy as np

users = pd.read_csv("users.csv")
orders = pd.read_csv("orders.csv")

sums_by_users = orders.groupby("user_id")["price"].sum()

users = users.merge(sums_by_users, on="user_id", how="left").fillna(0)

totals_by_city = users.groupby("city")["price"].mean()

print(totals_by_city)