import numpy as np

def neighbors(v, eps, X):
    return np.sum((X - v) ** 2, axis=1) <= eps

def spread(v, eps, k, X, min_samples, labels):
    ids = neighbors(v, eps, X)
    if ids.sum() < min_samples:
        return
    for i in range(X.shape[0]):
        if labels[i] == -1 and ids[i]:



def dbscan(X, eps = 0.5, min_samples = 5)
    n = X.shape[0]
    dists = np.sum((X[:, None, :] - X[None, :, :]) ** 2, axis=2)
    labels = np.zeros(n)
    labels.fill(-1)
    k = 0
    for i in range(n):
        if labels[i] != -1:
            continue
        labels[i] = k
