import numpy as np
from sklearn.tree import DecisionTreeClassifier

def max_correct_predictions(x, y):
    ind = np.argsort(x)
    x1 = x[ind].tolist()
    y1 = y[ind].tolist()
    i = 0
    ans = 0
    while i < len(x):
        c = [0, 0]
        while i < len(x) - 1 and x1[i] == x1[i + 1]:
            c[y1[i]] += 1
            i += 1
        c[y1[i]] += 1
        ans += max(c[0], c[1])
        i += 1
    return ans


n = int(input())
x = []
y = []
for i in range(n):
    a, b = map(int, input().split())
    x.append(a)
    y.append(b)
print(max_correct_predictions(np.array(x), np.array(y)))