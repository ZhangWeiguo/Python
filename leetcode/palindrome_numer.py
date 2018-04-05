'''
Determine whether an integer is a palindrome.
'''
class Solution(object):
    def isPalindrome(self, x):
        L = list(str(x))
        N = len(L)
        for i in range(N/2):
            if L[i] != L[N-i-1]:
                return False
        return True