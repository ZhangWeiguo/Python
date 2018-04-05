'''
find the longest common prefix string amongst an array of strings.
'''

class Solution(object):
    def longestCommonPrefix(self, strs):
        s = ""
        N1 = len(strs)
        if N1 ==0 :
            return s
        else:
            N2 = len(strs[0])
        for i in range(N2):
            s1 = strs[0][i]
            for j in range(1,N1):
                try:
                    if strs[j][i] != s1:
                        return s
                except:
                    return s
            s += s1
        return s