# -*-encoding:utf-8-*-

def Partition(L1, start, end):
    while start < end:
        while L1[start] <  L1[end] and start < end:
            start += 1
        if start < end:
            x = L1[start]
            L1[start] = L1[end]
            L1[end] = x
            end -= 1
        while L1[start] < L1[end] and start < end:
            end -= 1
        if start < end:
            x = L1[start]
            L1[start] = L1[end]
            L1[end] = x
            start += 1
    return end



def QuickSort(L):
    N = len(L)
    if N <= 1:
        pass
    else:
        i = Partition(L,0,N-1)
        L[0:i] = QuickSort(L[0:i])
        L[i:] = QuickSort(L[i:])
    return L

L1 = [4,3,28,8,9,10,4,2,1]
QuickSort(L1)


