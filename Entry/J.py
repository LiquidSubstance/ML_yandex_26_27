from itertools import permutations

def gen(a, i, p):
    global s
    if a == 0:
        c = p.copy()
        if len(p) == 5:
            s.append(c)
        return
    for j in range(i, a + 1):
        p.append(j)
        gen(a - j, j, p)
        p.pop()


s = []
m = 1e9
k = -1
for a1, a2, a3, a4, a5 in permutations([2, 4, 8, 16, 32]):
    c = a1 * a2 + a2 * a3 + a3 * a4 + a4 * a5
    m = min(m, c)
    k = max(k, c)
min1 = []
max1 = []
for a1, a2, a3, a4, a5 in permutations([2, 4, 8, 16, 32]):
    c = a1 * a2 + a2 * a3 + a3 * a4 + a4 * a5
    if c == m:
        min1.append((a1, a2, a3, a4, a5))
    if c == k:
        max1.append((a1, a2, a3, a4, a5))
m1 = 1e9
k1 = -1
gen(15, 1, [])
for p in s:
    for a1, a2, a3, a4, a5 in permutations(p):
        c = 2 ** (a1 + a2) + 2 ** (a2 + a3) + 2 ** (a3 + a4) + 2 ** (a4 + a5)
        m1 = min(m1, c)
        k1 = max(k1, c)
min2 = []
max2 = []
for p in s:
    for a1, a2, a3, a4, a5 in permutations(p):
        c = 2 ** (a1 + a2) + 2 ** (a2 + a3) + 2 ** (a3 + a4) + 2 ** (a4 + a5)
        if c == m1:
            min2.append((2 ** a1, 2 ** a2, 2 ** a3, 2 ** a4, 2 ** a5))
        if c == k1:
            max2.append((2 ** a1, 2 ** a2, 2 ** a3, 2 ** a4, 2 ** a5))
print(m, k, m1, k1)
min1 = sorted(list(set(min1)))
min2 = sorted(list(set(min2)))
max1 = sorted(list(set(max1)))
max2 = sorted(list(set(max2)))
for i in min1:
    print(*i)
for i in max1:
    print(*i)
for i in min2:
    print(*i)
for i in max2:
    print(*i)