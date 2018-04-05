'''
Given an array S of n integers, find three integers in S such that the sum is closest to a given number, target.
Return the sum of the three integers. You may assume that each input would have exactly one solution.

For example, given array S = {-1 2 1 -4}, and target = 1.
The sum that is closest to the target is 2. (-1 + 2 + 1 = 2).

'''
class Solution(object):
    def threeSumClosest(self, nums, target):
        min_distance = abs(nums[0] + nums[1] + nums[2] - target)
        best_target = nums[0] + nums[1] + nums[2]
        L = nums
        L.sort()
        N = len(L)
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
                a0 = L[i]+L[j]+a
                x = a0-target

                if(min_distance>abs(x)):
                    min_distance = abs(x)
                    best_target = a0
                    print best_target

                if x == 0:
                    return best_target
                elif x > 0:
                    j -= 1
                elif x < 0:
                    i += 1
        return best_target