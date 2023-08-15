def che(s):
    for i in range(len(s)):
        for j in range(i+1, len(s)):
            for k in range(j+1, len(s)):
                if s[i]+s[k] == 2*s[j]:
                    return False
    return True


a = [1, 9, 5, 3, 7, 2, 10, 6, 4, 8]
print(che(a))
