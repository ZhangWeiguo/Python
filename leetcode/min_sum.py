# -*- encoding:utf-8 -*-

'''
小易邀请你玩一个数字游戏，小易给你一系列的整数。
你们俩使用这些整数玩游戏。每次小易会任意说一个数字出来，
然后你需要从这一系列数字中选取一部分出来让它们的和等于小易所说的数字。 
例如： 如果{2,1,2,7}是你有的一系列数，小易说的数字是11.
你可以得到方案2+2+7 = 11.如果顽皮的小易想坑你，他说的数字是6，
那么你没有办法拼凑出和为6 现在小易给你n个数，
让你找出无法从n个数中选取部分求和的数字中的最小数（从1开始）。
'''
N = int(raw_input())
L = map(int,raw_input().split())

L.sort()
sumL = 0
for i in range(N):
    if L[i] > sumL + 1:
        break
    else:
        sumL += L[i]
print sumL + 1

