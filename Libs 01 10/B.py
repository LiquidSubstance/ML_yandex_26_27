import numpy as np

def k_nearest_neighbors(X, k):
    n, d = X.shape
    dist = np.sum((X[None, :, :] - X[:, None, :]) ** 2, axis=2)
    i = np.arange(n)
    i = i[:, None] + np.zeros((n, n))
    np.fill_diagonal(dist, 1e18)
    ans = np.lexsort((i, dist), axis=1)
    return ans[:, :k]

a = np.array([[1, 2], [3, 4], [5, 6], [7, 8], [9, 10], [11, 12], [-1, 15], [-10, 6], [1, 5], [6, 2]])
print(k_nearest_neighbors(a, 2))