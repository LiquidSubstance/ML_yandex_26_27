import pandas as pd

def is_negative(row):
    if row["Half"] == "-" or row["Official Time"] == "-":
        return 0
    to_half = pd.to_timedelta(row["Half"])
    from_half = pd.to_timedelta(row["Official Time"]) - to_half
    return to_half > from_half

splits = pd.read_csv("4_marathon.csv")[["Half", "Official Time"]].apply(lambda row : is_negative(row), axis=1)
print(splits.sum())
