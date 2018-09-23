# -*- encoding:utf-8 -*-
'''
题目描述
假定一种编码的编码范围是a ~ y的25个字母，从1位到4位的编码，如果我们把该编码按字典序排序，形成一个数组如下： 
a, aa, aaa, aaaa, aaab, aaac, … …, b, ba, baa, baaa, baab, baac … …, yyyw, yyyx, yyyy 
其中a的Index为0，aa的Index为1，aaa的Index为2，以此类推。 编写一个函数，输入是任意一个编码，
输出这个编码对应的Index.
输入描述:
输入一个待编码的字符串,字符串长度小于等于100.
输出描述:
输出这个编码的index
'''



def cal(s,n):
    t = 0
    x = ord(s) - 97
    if n == 0:
        t = x * (1+25*(1+25*26))
    elif n == 1:
        t = 1+x*25*(1+25*26)
    elif n == 2:
        t = 1+x*26
    elif n == 3:
        t = x+1
    return t
        


S = raw_input()
n = 0
N = len(S)
for i in range(4):
    if i >= N:
        break
    s = S[i]
    n += cal(s,i)
print n