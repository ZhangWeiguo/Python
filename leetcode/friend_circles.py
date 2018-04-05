'''
https://leetcode.com/problems/friend-circles/description/

 There are N students in a class. Some of them are friends,
 while some are not. Their friendship is transitive in nature.
 For example, if A is a direct friend of B, and B is a direct friend of C,
 then A is an indirect friend of C. And we defined a friend circle is
 a group of students who are direct or indirect friends.

Given a N*N matrix M representing the friend relationship
between students in the class. If M[i][j] = 1, then the ith and jth students are direct friends with each other,
otherwise not. And you have to output the total number of friend circles among all the students.
'''

class Solution(object):
    def findCircleNum(self, M):
        N = len(M)
        Num = 0
        S = range(N)
        def fun(k,a,N,S):
            S.remove(k)
            for i in range(N):
                if a[k][i] != 0 and k != i and i in S:
                    fun(i,a,N,S)
        while True:
            if len(S) == 0:
                break
            k = S[0]
            fun(k,M,N,S)
            Num += 1
        return Num