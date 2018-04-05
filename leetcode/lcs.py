# -*- encoding:utf-8 -*-
import numpy



'''
LCS 最大公共子序列
LCCS 最大公共子串
Manacher 最长回文子串
KMP 最长子串匹配
'''


class CS:
    def __init__(self):
        pass
    @staticmethod
    def LCS(s1,s2):
        N1 = len(s1)
        N2 = len(s2)
        Len = numpy.zeros((N1+1, N2+1))
        Dire = numpy.zeros((N1+1, N2+1))
        if N1 == 0 or N2 == 0:
            max_len = 0
            max_str = ""
        else:
            for i in range(1,N1+1):
                for j in range(1,N2+1):
                    if s1[i-1] == s2[j-1]:
                        Len[i,j] = Len[i-1,j-1] + 1
                        Dire[i,j] = 1
                    else:
                        a1 = Len[i-1,j]
                        b1 = Len[i,j-1]
                        if a1>b1:
                            Len[i,j] = a1
                            Dire[i,j] = 2
                        else:
                            Len[i,j] = b1
                            Dire[i,j] = 3
        max_len = int(Len[N1, N2])
        S = ""
        while N1>=1 and N2 >=1 :
            if Dire[N1, N2] == 1:
                S = s1[N1-1] + S
                N1 -= 1
                N2 -= 1
            elif Dire[N1, N2] == 2:
                N1 -= 1
            elif Dire[N1, N2] == 3:
                N2 -= 1
        max_str = S
        return max_len, max_str

    @staticmethod
    def LCCS(s1,s2):
        max_len = 0
        max_str = ""
        last_locate = 0
        N1 = len(s1)
        N2 = len(s2)
        Len = numpy.zeros((N1+1, N2+1))
        if N1 == 0 or N2 == 0:
            return max_len,max_str
        else:
            for i in range(1,N1+1):
                for j in range(1,N2+1):
                    if s1[i-1] == s2[j-1]:
                        Len[i,j] = Len[i-1,j-1] + 1
                        if max_len < Len[i,j]:
                            max_len = Len[i,j]
                            last_locate = i-1
                    else:
                        Len[i,j] = 0
            max_len = int(max_len)
            last_locate += 1
            max_str = s1[last_locate-max_len:last_locate]
            return max_len, max_str
    @staticmethod
    def Manacher(s):
        N = len(s)
        if N == 1:
            return s
        L = []
        for i in range(N):
            if i == 0:
                L.append('#')
            L.append(s[i])
            if i == N - 1:
                L.append('#')
            else:
                L.append('#')
        NN = len(L)
        id = 0
        mx = 0
        P = [0] * NN
        P[0] = 1
        P[NN - 1] = 1
        for i in range(1, NN - 1):
            if mx > i:
                P[i] = min([P[2 * id - i], mx - i])
            else:
                P[i] = 1
            k = 1
            while i - P[i] - k + 1 >= 0 and i + P[i] + k - 1 <= NN - 1:
                if L[i - P[i] - k + 1] == L[i + P[i] + k - 1]:
                    P[i] += 1
                else:
                    break
            if P[i] + i > mx:
                mx = P[i] + i
                id = i
        mx = max(P)
        id = P.index(mx)
        s = ''
        for i in range(mx):
            si = L[id + i]
            if si == "#":
                pass
            else:
                if i == 0:
                    s = s + si
                else:
                    s = si + s + si
        return s

    @staticmethod
    def Kmp(S0, S):
        def common(s,n):
            if n == 1:
                return 0
            i = 1
            k = 0
            while True:
                if s[0:i] == s[n-i:n]:
                    k = i
                i += 1
                if i >= n-1:
                    break
            return k

        if len(S) == 0 or len(S0) == 0:
            return -1
        i = 0
        j = 0
        k = 0
        N0 = len(S0)
        N = len(S)
        C = []
        for i in range(N):
            C.append(common(S[:i+1],i+1))
        i = 0
        while True:
            while True:
                if i > N0-1:
                    break
                j = C[k]
                if S0[i] == S[k]:
                    i += 1
                    k += 1
                else:
                    if k == 0:
                        i += 1
                    else:
                        j = C[k-1]
                        break
                if k > N - 1:
                    return i - 1 - N
            if k > N -1:
                break
            else:
                k = j
            if i > N0-1:
                return -1
        return i - N




# s1 = "abdcdfgggvt"
# s2 = "dgfabcdcdfg"
# s1 = "zhangweiguo"
# s2 = "wozhangsan"
# print CS.LCCS(s1,s2)
s0 = 'BBC ABCDAB ABCDABCDABDE'
s = 'ABCDABD'
print CS.Kmp(s0, s)