# -*- encoding:utf-8 -*-

'''
我们可以用2*1的小矩形横着或者竖着去覆盖更大的矩形。请问用n个2*1的小矩形无重叠地覆盖一个2*n的大矩形，总共有多少种方法？
'''

L = {}
class Solution:
    def rectCover(self, number):
        if number in L:
            return L[number]
        
        if number == 0:
            L[0] = 0
            return 0
        elif number == 1:
            L[1] = 1
            return 1
        elif number == 2:
            L[2] = 2
            return 2
        else:        
            m1 = self.rectCover(number-1)
            m2 = self.rectCover(number-2)
            L[number-1] = m1
            L[number-2] = m2
            return m1 + m2

S = Solution()
print S.rectCover(3)