def max_unique_run_length(s):
    n = len(s)
    if n == 0:
        return 0
    i = 0
    mx = 0
    a = set()
    for j in range(n):
        while s[j] in a:
            a.remove(s[i])
            i += 1
        a.add(s[j])
        mx = max(mx, j - i + 1)
    return mx
