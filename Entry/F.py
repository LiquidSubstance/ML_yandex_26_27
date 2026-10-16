import numpy as np

def pairwise_euclidean_distances(vectors):
    n, d = vectors.shape
    dist = np.zeros((n, n))

    for i in range(n):
        for j in range(n):
            t = 0
            for k in range(d):
                t += (vectors[i][k] - vectors[j][k]) ** 2
            dist[i, j] = np.sqrt(t)
    return dist