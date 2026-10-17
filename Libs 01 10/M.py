import pandas as pd
import numpy as np

def fill_na(row):
    if np.isnan(row["Age"]):
        row["Age"] = medians[row["Pclass"]][row["Sex"]]
    return row

data = pd.read_csv("titanic.csv")
medians = data.groupby(["Pclass", "Sex"])["Age"].median()
data = data.apply(lambda row: fill_na(row), axis=1)
data.to_csv("submissionM.csv")
print(np.sum(data["Age"]))