
def path(x, y, p):
    global used, ans

    if len(p) == 11:
        if p[-1] == (4, 2) and (0, 2) in p:
            ans += 1
        return

    if x > 0 and not used[x - 1][y]:
        p.append((x - 1, y))
        used[x - 1][y] = True
        path(x - 1, y, p)
        p.pop()
        used[x - 1][y] = False

    if x < 4 and not used[x + 1][y]:
        p.append((x + 1, y))
        used[x + 1][y] = True
        path(x + 1, y, p)
        p.pop()
        used[x + 1][y] = False

    if y > 0 and not used[x][y - 1]:
        p.append((x, y - 1))
        used[x][y - 1] = True
        path(x, y - 1, p)
        p.pop()
        used[x][y - 1] = False

    if y < 4 and not used[x][y + 1]:
        p.append((x, y + 1))
        used[x][y + 1] = True
        path(x, y + 1, p)
        p.pop()
        used[x][y + 1] = False

used = [[False] * 5 for _ in range(5)]
used[2][2] = True
ans = 0
path(2, 2, [(2, 2)])
print(ans)