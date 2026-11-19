import numpy as np

def mse(x, y):
    return np.sum((x - y) ** 2) / x.shape[0]

def best_threhshold(a):
    best_t = -1
    best_mse = 1e18
    for i in range(a.shape[0] - 1):
        left = a[0 : i + 1]
        right = a[i + 1 :]
        if len(left) and len(right):
            pred = np.zeros(len(a))
            pred[: i + 1] = left.mean()
            pred[i + 1 :] = right.mean()
            # print(left, right)
            # print(pred)
            # print(mse(pred, a))
            if mse(pred, a) < best_mse:
                best_mse = mse(pred, a)
                best_t = i + 1
    return best_t

def gen(max_k, l, r):
    global cur_k, ans, a, predictions
    if cur_k == max_k:
        return
    cur_k += 1
    t = best_threhshold(a[l : r])
    if t == -1:
        return
    # print(predictions)
    # print(a[l : r], l, r)
    # print(a[l : l + t], a[l + t : r])
    # print(t)
    predictions[l : l + t] = a[l : l + t].mean()
    predictions[l + t : r] = a[l + t : r].mean()
    err_l = np.sum((predictions[l : l + t] - a[l : l + t]) ** 2)
    err_r = np.sum((predictions[l + t : r] - a[l + t : r]) ** 2)
    if err_l > err_r:
        gen(max_k, l, l + t)
    else:
        gen(max_k, l + t, r)
n, k = map(int, input().split())
a = np.array(list(map(int, input().split())))
cur_k = 1
predictions = np.zeros(n)
ans = []
gen(k, 0, n)
# print(predictions)
print(np.sum((predictions - a) ** 2) / n)