import numpy as np

def best_threshold_by_cost(probabilities, y, thresholds, c_fn, c_fp):
    probabilities = np.array(probabilities, dtype=float)
    y = np.array(y, dtype=int)
    thresholds = np.array(thresholds, dtype=float)

    mn_cost = 1e18
    mn_t = -1
    i = 1
    for t in thresholds:
        prediction = (probabilities >= t).astype(int)
        confusion_matrix = np.zeros((2, 2))
        np.add.at(confusion_matrix, (prediction, y), 1)
        fp = confusion_matrix[1][0]
        fn = confusion_matrix[0][1]
        cost = fp * c_fp + fn * c_fn
        if cost < mn_cost:
            mn_t = i
            mn_cost = cost
        i += 1
    return mn_t, int(mn_cost)

n, k, c_fn, c_fp = map(int, input().split())
p = []
l = []
for i in range(n):
    u, v = map(float, input().split())
    p.append(u)
    l.append(v)
t = list(map(float, input().split()))
print(*best_threshold_by_cost(p, l, t, c_fn, c_fp))