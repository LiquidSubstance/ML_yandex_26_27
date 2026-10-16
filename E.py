import random

points = [tuple(sorted((random.random(), random.random(), random.random()))) for _ in range(100000)]

def est(a, b, c):
    good = 0
    for x, y, z in points:
        if x < a < y < b < z < c:
            good += 1

    return good / 10000

def gen():
    x = random.random()
    y = random.random()
    a = min(x, y)
    b = max(x, y)
    return tuple(sorted((a, b - a, 1 - b)))


ans = 0
for _ in range(100):
    a, b, c = gen()
    v = est(a, b, c)
    ans = max(ans, v)
print(ans)