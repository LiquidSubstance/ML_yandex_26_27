import numpy as np

def pairwise_distances(X):
    return np.sqrt(np.sum((X[None, :, :] - X[:, None, :]) ** 2, axis=2))
