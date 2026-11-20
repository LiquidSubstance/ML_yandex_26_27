import numpy as np
from sklearn.datasets import make_blobs
import matplotlib.pyplot as plt
def neighbors(v, eps, X):
    return np.sum((X - v) ** 2, axis=1) <= eps

def spread(v, eps, k, X, min_samples, labels):
    return



def dbscan(X, eps = 0.5, min_samples = 5):
    n = X.shape[0]
    labels = np.zeros(n)
    labels.fill(-1)
    point_labels = np.zeros(n).astype(int)
    for i in range(n):
        if neighbors(X[i], eps, X).sum() >= min_samples:
            point_labels[i] = 1
    for i in range(n):
        near = neighbors(X[i], eps, X)
        if near.sum() < min_samples and point_labels[near].sum() != 0:
            point_labels[i] = 2
        elif near.sum() < min_samples:
            point_labels[i] = 0
    adj = np.zeros((n, n))
    for i in range(n):
        if point_labels[i] == 1:
            near = neighbors(X[i], eps, X)
            adj[i, near[point_labels == 1]] = 1
            adj[near[point_labels == 1], i] = 1



X, _ = make_blobs(1000, 2, centers = 4, cluster_std=[2, 3, 1.8, 1.2])
labels = dbscan(X)
fig = plt.figure()
ax1 = fig.add_subplot()
ax1.scatter(X[:, 0], X[:, 1], c = labels, cmap="tab20c")
plt.show()