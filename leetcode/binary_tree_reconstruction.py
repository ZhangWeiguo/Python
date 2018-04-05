# -*-encoding:utf8-*-#
class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None

class Solution:
    def reConstructBinaryTree(self, pre, tin):
        def fun(A,p,t):
            if len(p) == 1 :
                A.val = p[0]
                return
            x = p[0]
            A.val = x
            n = t.index(x)
            tt0 = t[0:n]
            tt1 = t[n+1:]
            pp0 = []
            pp1 = []
            for i in p:
                if i in tt0:
                    pp0.append(i)
                elif i in tt1:
                    pp1.append(i)
            A0 = TreeNode(0)
            A1 = TreeNode(0)
            A.left = A0
            A.right = A1
            if len(pp0) != 0:
                fun(A0,pp0,tt0)
            else:
                A.left = None
            if len(pp1) != 0:
                fun(A1,pp1,tt1)
            else:
                A.right = None
        A = TreeNode(0)
        fun(A,pre,tin)
        return A

def PrintTree(A):
    if A != None:
        print A.val
        PrintTree(A.left)
        PrintTree(A.right)
P = [1,2,4,3,5,6]
T = [4,2,1,5,3,6]
S = Solution()
A = S.reConstructBinaryTree(P,T)
PrintTree(A)
