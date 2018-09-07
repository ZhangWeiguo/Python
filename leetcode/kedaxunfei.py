import sys



def cal_night(L,N):
    x = 0
    while True:
        L1 = []
        n = 0
        for i in range(N):
            if i == 0 or L[i] >= L[i-1]:
                L1.append(L[i])
                n += 1
        if n == N:
            break
        else:
            x += 1
        N = n
        L = L1
    return x

    

N = int(raw_input())
L = raw_input().split()
L = [int(i) for i in L]
n = cal_night(L,N)
sys.stdout.write(str(n))

