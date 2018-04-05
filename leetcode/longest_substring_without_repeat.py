'''
Given a string, find the length of the longest substring without repeating characters.

Examples:
Given "abcabcbb", the answer is "abc", which the length is 3.
Given "bbbbb", the answer is "b", with the length of 1.
Given "pwwkew", the answer is "wke", with the length of 3. Note that the answer must be a substring,
"pwke" is a subsequence and not a substring.
'''

class Solution(object):
    def lengthOfLongestSubstring(self, s):
        N = len(s)
        M = len(set(s))
        L = 0
        i = 0
        while i<N:
            if i+L >=N:
                break
            D = set([])
            D.add(s[i])
            for j in range(i+1,N):
                if s[j] in D:
                    break
                else:
                    D.add(s[j])
            L = max([L,len(D)])
            if L == M:
                break
            i += 1
        return L