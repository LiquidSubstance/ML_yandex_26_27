import pandas as pd
import numpy as np
data = pd.read_csv("titanicJ.csv")
data = data[data["Age"] > 18]
data = data.sort_values(["Fare", "PassengerId"], ascending=[False, True])
print(data.head())
submission = pd.DataFrame(columns=["rank", "PassengerId"])
submission["rank"] = [1, 2, 3]
ids = np.array(data["PassengerId"].head(3))
submission["PassengerId"] = ids
submission.to_csv("submissionJ.csv")
print(ids)