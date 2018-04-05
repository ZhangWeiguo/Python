#-*-encoding:utf-8-*-

def Sift(L, start, end):
    i = start
    j = (i+1)*2 - 1
    k = j+1
    while j <= end:
        if k <= end:
            if L[j] >= L[k]:
                j = k
        if L[i] > L[j]:
            x = L[i]
            L[i] = L[j]
            L[j] = x
            i = j
            j = (i + 1) * 2 - 1
            k = j + 1
        else:
            return L
    return L

def HeapSort(L):
    N = len(L)
    for i in range(N/2,0,-1):
        L = Sift(L,i-1,N-1)
    for i in range(1,N):
        L[i:] = Sift(L[i:],0,N-i-1)

L = [4,6,1,7,5,4,-9,10,34]
HeapSort(L)
print L
