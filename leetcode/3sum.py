'''
Given an array S of n integers, are there elements a, b, c in S such that a + b + c = 0?
Find all unique triplets in the array which gives the sum of zero.
Note: The solution set must not contain duplicate triplets.

For example, given array S = [-1, 0, 1, 2, -1, -4],
A solution set is:
[
  [-1, 0, 1],
  [-1, -1, 2]
]

'''
class Solution(object):
    def threeSum(self, nums):
        L = nums
        L.sort()
        N = len(L)
        LL = []
        L2 = []
        for k in range(N):
            a = L[k]
            if a in L2:
                continue
            else:
                L2.append(a)
            i = k+1
            j = N-1
            while (i<j):
                if ( i>k+1 and L[i] == L[i-1] ):
                    i += 1
                    continue
                a0 = L[i]+L[j]
                # print a,i,j,L[i],L[j],a0
                if a0 == -a:
                    LL.append([a,L[i],L[j]])
                    i += 1
                    j -= 1
                elif a0 > -a:
                    j -= 1
                elif a0 < -a:
                    i += 1
        return LL
