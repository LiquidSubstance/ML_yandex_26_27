import numpy as np
class KMeansCustom:
    def __init__(self, k=3, max_iters=1000, tol=1e-4):
        self.k = k
        self.max_iters = max_iters
        self.tol = tol
        self.centroids = None

    def fit(self, X):
        rng = np.random.default_rng(42)
        self.centroids = X[rng.choice(X.shape[0], self.k, replace=False)].astype(float)
        for _ in range(self.max_iters):
            new_centroids = np.zeros((self.k, X.shape[1])).astype(float)
            labels = np.argmin(np.sum((self.centroids[None, :, :] - X[:, None, :]) ** 2, axis = 2), axis = 1).astype(int)
            for i in range(self.k):
                points = X[labels == i]
                if len(points) == 0:
                    new_centroids[i] = X[rng.integers(X.shape[0])]
                else:
                    new_centroids[i] = points.mean(axis = 0)
            if abs(new_centroids - self.centroids).max() < self.tol:
                self.centroids = new_centroids
                break
            self.centroids = new_centroids
        return self

    def predict(self, X):
        labels = np.argmin(np.sum((self.centroids[None, :, :] - X[:, None, :]) ** 2, axis = 2), axis = 1).astype(int)
        return labels