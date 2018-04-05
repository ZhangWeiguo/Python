'''
Given an array S of n integers, are there elements a, b, c, a
nd d in S such that a + b + c + d = target?
Find all unique quadruplets in the array which gives the sum of target.

Note: The solution set must not contain duplicate quadruplets.

For example, given array S = [1, 0, -1, 0, -2, 2], and target = 0.
A solution set is:
[
  [-1,  0, 0, 1],
  [-2, -1, 1, 2],
  [-2,  0, 0, 2]
]

'''

import copy
def threeSum(nums,target):
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
            if a0 == target-a:
                LL.append([a,L[i],L[j]])
                i += 1
                j -= 1
            elif a0 > target-a:
                j -= 1
            elif a0 < target-a:
                i += 1
    return LL
class Solution(object):
    def fourSum(self, nums, target):
        LL = []
        L2 = []
        L3 = []
        nums.sort()
        T = copy.copy(nums)
        N = len(nums)
        for i in range(N):
            a0 = nums[i]
            a1 = target-nums[i]
            if a0 in L2:
                continue
            else:
                L2.append(a0)
            T.remove(a0)
            L1 = threeSum(T, a1)
            for i in L1:
                i.append(a0)
                if set(i) not in L3:
                    LL.append(i)
                    L3.append(set(i))
        return LL