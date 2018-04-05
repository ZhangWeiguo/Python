# -*-encoding:utf8-*-

'''
Given n non-negative integers a1, a2, ..., an, where each represents a point at coordinate (i, ai).
n vertical lines are drawn such that the two endpoints of line i is at (i, ai) and (i, 0).
Find two lines, which together with x-axis forms a container, such that the container contains the most water.
'''

class Solution(object):
    def maxArea(self, height):
        N = len(height)
        max_area = 0
        i = 0
        j = N-1
        while (i<j):
            s = (j-i)*min([height[i],height[j]])
            if s > max_area:
                max_area = s
            if height[i] > height[j]:
                j -= 1
            else:
                i += 1
        return max_area