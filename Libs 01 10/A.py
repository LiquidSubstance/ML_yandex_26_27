import numpy as np
import pandas as pd

def to_permille(x):
    return np.floor(x * 1000 + 0.5).astype(int)

data = pd.read_csv("predictions.csv")
confusion_matrix = np.zeros((5, 5))
np.add.at(confusion_matrix, (data["y_true"], data["y_pred"]), 1)
print(confusion_matrix)
support = np.sum(confusion_matrix, axis=1).astype(int)
TP = confusion_matrix.diagonal()
FP = np.sum(confusion_matrix, axis=0) - TP
FN = np.sum(confusion_matrix, axis=1) - TP
precision = TP / (TP + FP)
recall = TP / (TP + FN)
f1 = 2 * precision * recall / (recall + precision)
submission = pd.DataFrame({"class": [0, 1, 2, 3, 4],
                            "support": support,
                            "precision": to_permille(precision),
                            "recall": to_permille(recall),
                            "f1": to_permille(f1),
                            })
submission.to_csv("submissionA.csv")