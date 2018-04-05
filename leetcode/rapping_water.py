
class Solution(object):
    def trap(self, height):
        N = len(height)
        if N <= 2:
            return 0
        S = 0
        X = 0
        S0 = 0
        i = 0
        j = N-1
        a0 = height[0]
        k = 0
        direct = True
        while True:
            print i,j,X,S
            if i == j:
                if direct == False:
                    j = k
                    direct = True
                    a0 = height[i]
                    k = i
                    X = 0
                    S0 = 0
                else:
                    i = k
                    direct = False
                    a0 = height[j]
                    k = j
                    X = 0
                    S0 = 0
            if direct:
                i += 1
                if height[i] >= a0:
                    S0 = (i-k-1)*min([a0,height[i]]) - X
                    S += S0
                    if i == j:
                        break
                    direct = False
                    a0 = height[j]
                    k = j
                    X = 0
                    S0 = 0
                else:
                    X += height[i]
            else:
                j -= 1
                if height[j] >= a0:
                    S0 = (k-j-1)*min([a0,height[j]]) - X
                    S += S0
                    if i == j:
                        break
                    direct = True
                    a0 = height[i]
                    k = i
                    X = 0
                    S0 = 0
                else:
                    X += height[j]
        return S