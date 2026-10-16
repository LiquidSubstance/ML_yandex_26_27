import numpy as np

class KMeans:
    def __init__(self, n_clusters, max_iter: int = 300, random_state: int= 42):
        self.n_clusters = n_clusters
        self.max_iter = max_iter
        self.random_state = random_state
        self.centroids = None
        self.labels = None

    def fit(self, X):
        n_samples, n_features = X.shape
        rng = np.random.RandomState(self.random_state)
        init_idx = rng.choice(n_samples, self.n_clusters, replace=False)
        self.centroids = X[init_idx].copy()

        for _ in range(self.max_iter):

            labels = np.empty(n_samples)

            for i in range(n_samples):
                dist = np.sum((self.centroids - X[i]) ** 2, axis=1)
                labels[i] = np.argmin(dist)

            new_centroids = np.zeros(self.n_clusters)
            

