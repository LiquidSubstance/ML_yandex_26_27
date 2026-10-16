import pandas as pd
import numpy as np

def std(column):
    a = np.array(column)
    return np.sqrt(np.sum((a - a.mean()) ** 2, axis=0) / len(column))

def add_z_score(row):
    c = int(row["class"]) - 1
    if stds[c] == 0:
        row["z_score"] = 0
        return row
    row["z_score"] = (int(row["score"]) - means[c]) / stds[c]
    return row

data = pd.read_csv("students.csv")
data["z_score"] = np.zeros(len(data))
print(data)
means = np.array(data.groupby("class")["score"].mean())
stds = np.array(data.groupby("class")["score"].apply(lambda column: std(column)))
print(means)
print(stds)
data = data.apply(lambda row: add_z_score(row), axis=1)
print(data)
data.to_csv("submissionK.csv")