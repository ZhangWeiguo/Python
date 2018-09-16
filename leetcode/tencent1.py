line = raw_input().split()
L = map(int,line)
X = L[0]
Y = L[1]
N = int((-1+(1+8*(X+Y))**(0.5))/2)
x = X
nx = 0 
for i in range(N):
    if x == 0:
        break
    score = N - i
    if score > x:
        continue
    else:
        nx += 1
        x -= score
if x == 0:
    print nx
else:
    print -1
