# -*- encoding:utf-8 -*-

K = int(raw_input())
A = raw_input()
B = raw_input()
n = 0
Na = len(A)
Nb = len(B)
S = set([])
for i in range(Na-K+1):
    x = A[i:i+K]
    if x not in S:
        S.add(x)
        
        if B.count(x) == 0:
            continue
        j = 0
        while j < Nb-K+1:
            if B[j:].count(x) == 0:
                break
            if B[j:j+K] == x:
                n += 1
                j += 1
            else:
                j += 1


print n