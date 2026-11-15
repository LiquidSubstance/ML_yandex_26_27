import pandas as pd
import numpy as np

def is_accelerating(row):
    if row["40K"] == "-" or row["35K"] == "-":
        return -1
    dist1 = 5000
    dist2 = 2195
    d1 = (pd.to_datetime(row["40K"]) - pd.to_datetime(row["35K"])).total_seconds()
    d2 = (pd.to_datetime(row["Official Time"]) - pd.to_datetime(row["40K"])).total_seconds()
    return int(dist2 / d2 > dist1 / d1)


def count_stat(group):
    a = group.apply(lambda row: is_accelerating(row), axis=1)
    vc = (a.value_counts()).reindex([1, 0, -1]).fillna(0)
    n = vc[1] + vc[0] - vc[-1]
    if n < 100:
        return -1
    return (vc[1] / n, vc[1])

data = pd.read_csv("4_marathon.csv")[["35K", "40K", "Age", "Official Time"]]
data["Age Group"] = data["Age"] // 10
accelerated = data.groupby(by="Age Group").apply(lambda group: count_stat(group))
print(accelerated)