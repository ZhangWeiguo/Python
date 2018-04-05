# -*-encoding:utf8-*-#
class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None

class Solution:
    def Mirror(self, root):
        def fun(A1, root1):
            if root1 != None:
                A1.val = root1.val
            if root1.left != None:
                A1.right = TreeNode(0)
                fun(A1.right, root1.left)
            if root1.right != None:
                A1.left = TreeNode(0)
                fun(A1.left, root1.right)
            return
        if root == None:
            A = None
        else:
            A = TreeNode(0)
            fun(A,root)
        return A

A0 = TreeNode(8)
A1 =  TreeNode(6)
A1.left = TreeNode(5)
A1.right = TreeNode(7)
A0.left = A1
A2 =  TreeNode(10)
A2.left = TreeNode(9)
A2.right = TreeNode(11)
A0.right = A2
S = Solution()
A1 = S.Mirror(A0)
print A1.val,A1.left.val,A1.right.val