# -*-encoding:utf8-*-#
class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None

class Solution:
    def reConstructBinaryTree(self, pre, tin):
        np = len(pre)
        nt = len(tin)
        if np == 0:
            return None
        elif np == 1:
            return TreeNode(pre[0])
        else:
            T0 = TreeNode(pre[0])
            t0 = pre[0]
            t0x = tin.index(t0)
            tin_left = tin[0:t0x]
            tin_right = tin[t0x:]
            pre_left = []
            pre_right = []
            for i in pre[1:]:
                
                if i in tin_left:
                    pre_left.append(i)
                else:
                    pre_right.append(i)
            print len(pre_left),len(tin_left),len(pre_right),len(tin_right)
            T_left = self.reConstructBinaryTree(pre_left, tin_left)
            T_right = self.reConstructBinaryTree(pre_right, tin_right)
            T0.left = T_left
            T0.right = T_right
            return T0

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
