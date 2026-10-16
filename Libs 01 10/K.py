import pandas as pd
import numpy as np
data = pd.read_csv("titanicJ.csv")

S = np.array(data["SibSp"])
P = np.array(data["Parch"])
data["FamilySize"] = S + P + 1
data = data[data["FamilySize"] >= 4]
survived = data[data["Survived"] == 1]
print(len(survived) / len(data))
