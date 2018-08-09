import sys

s = sys.stdin.readline().strip().split(",")
L = []
for n in s:
    try:
        x = int(n.strip())
        L.append(x)
    except:
        pass
N = len(L)
if N == 1:
    sys.stdout.write(str(L[0]))
elif N == 0:
    sys.stdout.write("0")
else:
    maxSum = L[0]
    for i in range(N):
        tmpSum = L[i]
        if tmpSum > maxSum:
            maxSum = tmpSum
        for j in range(i+1,N):
            tmpSum += L[j]
            if tmpSum > maxSum:
                maxSum = tmpSum
        if tmpSum > maxSum:
            maxSum = tmpSum
    sys.stdout.write(str(maxSum))



###################################

import sys
L = []

for i in range(21):
    s0 = sys.stdin.readline()
    L.append(int(s0.strip()))
N = len(L)
maxVal = 0
maxIndex = 0
for i in range(N-3):
    x = sum(L[i:i+4])
    if x > maxVal:
        maxVal = x
        maxIndex = i
sys.stdout.write(str(maxIndex))



###################################
import sys,copy

def maxInDistance(allData, N, indexs, distance):
    index = 0
    value = 0
    for i in indexs:
        for j in range(N):
            if j >= i -distance and j <= i + distance:
                if allData[j] > value:
                    value = allData[j]
                    index = j
    return index,value

N = 3
L = [7,4,9,7]
K = 3
d = 50

D1 = []
D2 = []
k = 1
while True:
    if k > K:
        break
    if k == 1:
        a = max(L)
        index = L.index(a)
        D1.append(a)
        D2.append([index])
    else:
        index = 0
        value = 0
        print D2,D1,k-2
        D20 = copy.deepcopy(D2[k-2])
        D10 = copy.deepcopy(D1[k-2])
        index, value = maxInDistance(L, N, D20, d)
        print index,value
        D20.append(index)
        print D20,D10
        D2.append(D20)
        D1.append(D10*value)
    k += 1
print D1[k-2]









###################################
import sys
def isPalindrome(S1,S2):
    S = S1 + S2
    N = len(S)
    if N <= 1:
        return True
    else:
        k = 0
        n = N/2
        L1 = list(S[0:n])
        if n*2 == N:
            L2 = list(S[n:])
        else:
            L2 = list(S[n+1:])
        
        L2.reverse()
        if L1 == L2:
            return True
        else:
            return False
            
L = []
k = 0
N = int(sys.stdin.readline().strip())
for i in range(N):
    s = sys.stdin.readline().strip()
    L.append(s)
for i in range(N):
    for j in range(N):
        if i != j and isPalindrome(L[i],L[j]):
            k += 1
print k