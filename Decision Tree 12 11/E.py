import numpy as np

def leaf_prediction(counts):
    c = np.array(counts).astype(float)
    return int(c.argmax()), (c / np.sum(c)).tolist()

n = int(input())
c = list(map(int, input().split()))
print(leaf_prediction(c)[0])
print(*leaf_prediction(c)[1])
