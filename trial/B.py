import numpy as np
X = np.zeros((60, 2))
X[:20, 1] = 1
X[20:50, 0] = 1
X[50:60, 1] = 1
X[50:60, 0] = 1
print(X)
print(X @ X.T)
print(np.linalg.matrix_power((X @ X.T), 3).trace())
