import sys,copy

  

line1 = map(int,raw_input().split())
n = line1[0]
k = line1[1]
L = map(int,raw_input().split())
D = map(int,raw_input().split())


y = sum([L[i] for i in range(n) if D[i] == 1])
maxValue = 0
for i in range(n):
    if D[i] == 0:
        maxValueTmp = sum([L[j] for j in range(i,min(i+k,n)) if D[j]==0])
        if maxValue < maxValueTmp+y:
            maxValue = maxValueTmp+y
        if maxValueTmp >= sum(L[i+1:]):
            break
print maxValue