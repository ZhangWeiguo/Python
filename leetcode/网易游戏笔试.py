import sys,copy

  
def move(k, L):
    D = []
    minValue = min(L)
    maxValue = max(L)
    minIndex = L.index(minValue)
    maxIndex = L.index(maxValue)
    stop = sum(L)%len(L)

    for i in range(k):
        if maxValue == minValue:
            return 0, D
        if maxValue - minValue == stop:
            break
        
        D.append((maxIndex+1,minIndex+1))
        L[minIndex] += 1
        L[maxIndex] -= 1
        minValue = min(L)
        maxValue = max(L)
        minIndex = L.index(minValue)
        maxIndex = L.index(maxValue)
    return maxValue - minValue, D


line1 = map(int,raw_input().split())
n = line1[0]
k = line1[1]
L = map(int,raw_input().split())
v,D = move(k, L)
print v,len(D)
for i,j in D:
    print i,j
        


