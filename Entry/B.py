def gen(a, i, p):

    global ans, primes

    if len(a) == i:
        if len(p) % 2 == 0:
            flag1 = True
            for j in p:
                if sum(j) not in primes:
                    flag1 = False
                    break
            if flag1:
                flag2 = True
                u = []
                for j in p:
                    if sum(j) in u:
                        flag2 = False
                        break
                    u.append(sum(j))
                if flag2:
                    ans += 1

        return

    x = a[i]

    for j in range(len(p)):
        p[j].append(x)
        gen(a, i + 1, p)
        p[j].pop()

    p.append([x])
    gen(a, i + 1, p)
    p.pop()

ans = 0
primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53]
gen([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 0, [])
print(ans)