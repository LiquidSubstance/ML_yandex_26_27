import pandas as pd
import csv
import numpy as np

data = pd.read_csv("titanic.csv")
a = data[data["Pclass"] == 1]["Fare"].mean()
b = data[data["Pclass"] == 2]["Fare"].mean()
c = data[data["Pclass"] == 3]["Fare"].mean()
submission = pd.DataFrame(columns=["Pclass", "mean_fare"])
submission["Pclass"] = [1, 2, 3]
submission["mean_fare"] = [a, b, c]
submission.to_csv("submissionI.csv")
