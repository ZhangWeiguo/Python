class Solution:
    def TreeDepth(self, pRoot):
        def fun(N,root):
            if root == None:
                return N
            else:
                if root.left != None:
                    N1 = N + 1
                    N1 = fun(N1,root.left)
                else:
                    N1 = N
                if root.right != None:
                    N2 = N + 1
                    N2 = fun(N2,root.right)
                else:
                    N2 = N
                N = max([N1,N2])
                return N
        if pRoot == None:
            return 0
        else:
            N = fun(1,pRoot)
        return N