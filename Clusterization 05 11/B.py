import numpy as np
# from sklearn.datasets import make_blobs
# import matplotlib.pyplot as plt


# class Kmeans_plus_plus:
#
#     def __init__(self, k, random_state=42):
#         self.k = k
#         self.random_state = random_state
#         self.centroids = None
#
#     def fit(self, X):
#         rng = np.random.default_rng(42)
#         self.centroids = np.empty((self.k, X.shape[1]))
#         remaining = np.ones(X.shape[0]).astype(bool)
#         indecies = np.arange(0, X.shape[0])
#         ind = rng.choice(X.shape[0])
#         self.centroids[0] = X[ind]
#         remaining[ind] = False
#         for i in range(1, self.k):
#             dists = np.sum((self.centroids[None, :, :] - X[:, None, :]) ** 2, axis=2).min(axis=1)
#             if np.sum(dists) > 0:
#                 ind = rng.choice(X.shape[0], p=dists / np.sum(dists))
#                 self.centroids[i] = X[ind]
#                 remaining[ind] = False
#             else:
#                 ind = rng.choice(indecies[remaining])
#                 self.centroids[i] = X[ind]
#                 remaining[ind] = False
#         return self
#
#     def predict(self, X):
#         labels = np.argmin(np.sum((self.centroids[None, :, :] - X[:, None, :]) ** 2, axis=2), axis=1).astype(int)
#         return labels

def kmeans_plus_plus(X, k, random_state=42):
    rng = np.random.default_rng(random_state)
    centroids = np.empty((k, X.shape[1])).astype(float)
    remaining = np.ones(X.shape[0]).astype(bool)
    indices = np.arange(0, X.shape[0])
    ind = rng.choice(X.shape[0])
    centroids[0] = X[ind]
    remaining[ind] = False
    d2 = np.sum((X - centroids[0]) ** 2, axis = 1)
    for i in range(1, k):
        if np.sum(d2) > 0:
            ind = rng.choice(X.shape[0], p=d2 / np.sum(d2))
            centroids[i] = X[ind]
            remaining[ind] = False
        else:
            ind = rng.choice(indices[remaining])
            centroids[i] = X[ind]
            remaining[ind] = False
        d2 = np.minimum(d2, np.sum((X - centroids[i]) ** 2, axis = 1))
    return centroids

# X, _ = make_blobs(n_samples=5000, n_features= 3, centers=4, cluster_std=[2, 1.8, 3.5, 2], random_state=40)
# K = Kmeans_plus_plus(4)
# K.fit(X)
# labels = K.predict(X)
# c1 = kmeans_plus_plus(X, 4)
# fig = plt.figure()
# ax1 = fig.add_subplot(projection='3d')
# og = c1
# i = int(input())
# if i:
#     og = K.centroids
#     K.centroids = c1
#     labels = K.predict(X)
# ax1.scatter(X[:, 0], X[:, 1], X[:, 2], c=labels, s=10, cmap='viridis')
# ax1.scatter(
#     K.centroids[:, 0], K.centroids[:, 1], K.centroids[:, 2], c='green',
#     s=200, marker='X', label='Центроиды',
# )
# ax1.scatter(
#     og[:, 0], og[:, 1], og[:, 2], c='red',
#     s=200, marker='D', label='Центроиды',
# )
# ax1.legend()
# plt.show()