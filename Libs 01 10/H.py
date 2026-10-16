import pandas as pd
import csv
import numpy as np

data = pd.read_csv("titanic.csv")
a = (len(data[data["Pclass"] == 1]))
b = (len(data[data["Pclass"] == 2]))
c = (len(data[data["Pclass"] == 3]))
submission = pd.DataFrame(columns=["Pclass", "passengers", "is_largest"])
submission["Pclass"] = [1, 2, 3]
submission["passengers"] = [a, b, c]
submission["is_largest"] = [0, 0, 1]
submission.to_csv("submissionH.csv")