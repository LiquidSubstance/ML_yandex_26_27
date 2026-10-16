import pandas as pd
import numpy as np

data = pd.read_csv("titanic.csv")
mask = ((data["Survived"] == 1) & (data["Sex"] == "female"))
print(data[mask]["Age"].mean())