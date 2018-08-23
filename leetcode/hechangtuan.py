# -*- encoding:utf-8 -*-
'''
有 n 个学生站成一排，每个学生有一个能力值，
牛牛想从这 n 个学生中按照顺序选取 k 名学生，
要求相邻两个学生的位置编号的差不超过 d，
使得这 k 个学生的能力值的乘积最大，你能返回最大的乘积吗？
'''

import sys

def iterMult(L):
    x = 1
    for i in L:
        x *= i
    return x


def maxValue(L, k, d, n0 = 0):
    L0 = []
    if len(L) == k:
        return iterMult(L)
    elif k == 1:
        mn = min(L)
        mx = max(L)
        if n0/2 == 0:
            return mx
        else:
            if mx <= 0:
                return mx
            elif mn >= 0:
                return mn
            else:
                return mn
    else:
        for i in range(0, len(L)-k+1):
            i0 = i + d
            i1 = len(L) - k + 1
            i2 = min(i0, i1)
            for j in range(i+1, i2):
                if L[i] < 0:
                    n0 += 1
                x = L[i] * maxValue(L[j:], k-1, d, n0)
                L0.append(x)
        return max(L0)



n=map(int,raw_input().split())[0]
line=map(int,raw_input().split())
K,d=map(int,raw_input().split())
fm=[[0 for i in range(K)] for i in range(n)]
fn=[[0 for i in range(K)] for i in range(n)]
ans=None
for i in range(0,n):
    fn[i][0]=fm[i][0]=line[i]
    for k in range(1,min(i+1,K)):
        for j in range(max(0,i-d),i):
            fm[i][k]=max(fm[i][k],max(fm[j][k-1]*line[i],fn[j][k-1]*line[i]))
            fn[i][k]=min(fn[i][k],min(fm[j][k-1]*line[i],fn[j][k-1]*line[i]))
    ans=max(ans,fm[i][K-1])
print ans


        
# if __name__ == "__main__":
#     nPerson = int(sys.stdin.readline().strip())
#     line = sys.stdin.readline().strip().split()
#     L = [int(i) for i in line]
#     line = sys.stdin.readline().strip().split()
#     k = int(line[0])
#     d = int(line[1])
#     print maxValue(L, k, d)


L = '7 -15 31 49 -44 35 44 -47 -23 15 -11 10 -21 10 -13 0 -20 -36 22 -13 -39 -39 -31 -13 -27 -43 -6 40 5 -47 35 -8 24 -31 -24 -1'
L = L.split()
L = [int(i) for i in L]
k = 3
d = 31

print maxValue(L, k, d)