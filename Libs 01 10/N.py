import pandas as pd
import numpy as np

def total_by_city(column):
    return np.sum(sums_by_users[column["user_id"]])

users = pd.read_csv("users.csv")
orders = pd.read_csv("orders.csv")

sums_by_users = orders.groupby("user_id")["price"].sum()
users_by_cities = pd.DataFrame(columns=["city", "total"])
