# -*-encoding:utf-8-*-
'''
‘º…™∑ÚŒ Ã‚
'''

def LastRemaining(n, m):
    if n == 0 or m == 0:
        return 0
    L = range(n)
    Init = 0
    n0 = n
    while True:
        print L
        print Init,n0
        if len(L) == 1:
            break
        if Init + m <= n0 - 1:
            L.pop(Init + m - 1)
            n0 = n0 - 1
            if Init + m -1 > n0 - 1:
                Init = 0
            else:
                Init = Init + m -1
        else:
            m0 = m - (n0 - 1 - Init)
            k = m0 / n0 + 1
            Init = n0-((k*n0)-m0%(k * n0)) -1
            L.pop(Init - 1)
            n0 = n0 - 1
            if Init == 0:
                Init = 0
            elif Init < 0:
                Init = n0 + Init
            else:
                Init = Init - 1

    return L[0]

print LastRemaining(5,2)