import random
import numpy as np

good1 = 0

for x in range(1):
    points = [random.random() for _ in range(1000000)]
    angles = [random.random() * np.pi for _ in range(1000000)]

    good = 0

    for i in range(1000000):
        dist1 = abs(points[i] / np.sin(angles[i]))
        dist2 = abs((1 - points[i]) / np.sin(angles[i]))
        if dist1 <= 0.3 or dist2 <= 0.3:
            good += 1
    print(good / 1000000)
    if 0.509 <= (good / 1000000) < 0.510:
        good1 += 1
print(good1)