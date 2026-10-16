def is_palindrome_after_one_removal(s):
    if len(s) == 0:
        return False
    if len(s) == 1:
        return True
    i = 0
    j = len(s) - 1
    while i < j:
        if s[i] != s[j]:
            if i != 0 and s[i : j] != s[j - 1 : i - 1 : -1] and s[i + 1 : j + 1] != s[j : i : -1]:
                return False
            elif i == 0 and s[i : j] != s[j - 1 : : -1] and s[i + 1 : j + 1] != s[j : i : -1]:
                return False
        i += 1
        j -= 1
    return True