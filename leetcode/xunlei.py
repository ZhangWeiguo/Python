import sys

def second():
    line = raw_input()
    L = map(int,line.split(","))
    N = len(L)
    if N < 3:
        sys.stdout.write("False")
        exit(0)
    for i in range(1,N-1):
        if sum(L[0:i]) == sum(L[i+1:]):
            sys.stdout.write(str(L[i]))
            exit(0)
    sys.stdout.write("False")


def first():
    line = raw_input()
    line1 = line.split("-")
    L1 = map(int, line1[0].split(","))
    line2 = line1[1].split(":")
    L2 = map(int, line2[0].split(","))
    K = int(line2[1])
    L1 = sorted(L1, reverse=True)
    L2 = sorted(L2, reverse=True)
    k1 = 0
    k2 = 0
    N1 = len(L1)
    N2 = len(L2)
    L = []
    k = 0
    for i in range(N1):
        for j in range(N2):
            L.append(L1[i]+L2[j])
    L = sorted(L,reverse=True)
    L = L[0:K]
    sys.stdout.write(','.join(map(str,L)))



line = raw_input()
line1 = line.split("-")
L1 = map(int, line1[0].split(","))
line2 = line1[1].split(":")
L2 = map(int, line2[0].split(","))
K = int(line2[1])
L1 = sorted(L1, reverse=True)
L2 = sorted(L2, reverse=True)
k1 = 0
k2 = 0
N1 = len(L1)
N2 = len(L2)
L = []
S = [0] * N2
for i in range(K):
    print k1,k2,N1,N2
    L.append(L1[k1]+L2[k2])
    S[k2] = k1 + 1

    if k1 >= N1:
        k2 += 1
        continue
    if k2 >= N2:
        k1 += 1
        continue
    if k1+1 >= N1:
        k2 += 1
        continue
    if k2+1 >= N2:
        k1 += 1
        continue
    if L1[k1] + L2[k2+1] > L1[S[k2]] + L2[k2]:
        k2 += 1
    else:
        k1 += 1
sys.stdout.write(','.join(map(str,L)))