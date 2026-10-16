import numpy as np
n, t = map(float, input().split())
n = int(n)
x = list(map(float, input().split()))
d = 0
m = -1e18
for i in range(n):
    m = max(m, x[i] / t)
for i in range(n):
    d += np.e**((x[i] / t) - m)
for i in range(n):
    print(np.e**((x[i] / t) - m) / d, sep=" ")