# -*-encoding:utf8-*-
'''
一只青蛙一次可以跳上1级台阶，也可以跳上2级……它也可以跳上n级。
求该青蛙跳上一个n级的台阶总共有多少种跳法。
'''
class Solution:
    def jumpFloorII(self, number):
        def Jump(Number):
            if Number == 0:
                return 1
            if Number == 1:
                return 1
            else:
                n = 0
                for i in range(1,Number+1):
                    n = n + Jump(Number - i)
                return n
        N = Jump(number)
        return N