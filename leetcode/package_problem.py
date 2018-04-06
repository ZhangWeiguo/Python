# -*- encoding:utf-8 -*-


# Given n items with size Ai, an integer m denotes the size of a backpack.
# How full you can fill this backpack?

def maxContent(weights, content):
    '''
    weights = [2,3,5,7]
    content = 12
    print maxContent(weights, content)
    '''
    N = len(weights)
    M = int(content)
    W = [[0]*(M+1) for i in range(N+1)]
    for i in range(1,N+1):
        for j in range(1,M+1):
            if j < weights[i-1]:
                W[i][j] = W[i-1][j]
            else:
                W[i][j] = max([W[i-1][j], W[i-1][j-weights[i-1]] + weights[i-1]])
    return W[i][j]
    


# 0-1 背包问题
# Given n items with size Ai and value Vi, and a backpack with size m.
# What's the maximum value can you put into the backpack?

# (1) 1D
def maxValue(weights, values, content):
    '''
    content = 10
    weights = [2,3,5,7]
    values = [1,5,2,4]
    print maxValue(weights, values, content)
    '''
    N = len(weights)
    M = int(content)
    W = [0]*(M+1)
    for i in range(N):
        for j in range(M,0,-1):
            if j >= weights[i]:
                W[j] = max([W[j-1], W[j-weights[i]] + values[i]])
    return W[M]

# (2) 2D
# def maxValue(weights, values, content):
#     '''
#     content = 10
#     weights = [2,3,5,7]
#     values = [1,5,2,4]
#     print maxValue(weights, values, content)
#     '''
#     N = len(weights)
#     M = int(content)
#     W = [[0]*(M+1) for i in range(N+1)]
#     for i in range(1,N+1):
#         for j in range(1,M+1):
#             if j < weights[i-1]:
#                 W[i][j] = W[i-1][j]
#             else:
#                 W[i][j] = max([W[i-1][j], W[i-1][j-weights[i-1]] + values[i-1]])
#     return W[i][j]



# 完全背包问题
#  Given n kind of items with size Ai and value Vi( each item has an infinite number available)
#  and a backpack with size m.
#  What's the maximum value can you put into the backpack?

# (1) 1D
def maxValueFullPackage(weights, values, content):
    '''
    content = 10
    weights = [2,3,5,7]
    values = [1,5,2,4]
    print maxValueFullPackage(weights, values, content)
    '''
    N = len(weights)
    M = int(content)
    W = [0]*(M+1)
    for i in range(N):
        for j in range(M+1):
            if j >= weights[i]:
                W[j] = max([W[j], W[j-weights[i]] + values[i]])
    return W[M]


# 多重背包问题
#  Given n kind of items with size Ai and value Vi( each item has an finite number available)
#  and a backpack with size m.
#  What's the maximum value can you put into the backpack?

def maxValueFinitePackage(weights, values, nums, content):
    '''
    content = 10
    weights = [2,3,5,7]
    values = [1,5,2,4]
    nums = [1,2,3,2]
    print maxValueFinitePackage(weights, values, nums, content)
    '''
    N = len(weights)
    M = int(content)
    W = [0]*(M+1)
    for i in range(N):
        for k in range(nums[i]):
            for j in range(M,0,-1):
                if j >= weights[i]:
                    W[j] = max([W[j], W[j-weights[i]] + values[i]])
    return W[M]


# 混合问题
# 有的取一次，有的取多次，有的无限次


##########################################################
# 二维费用
##########################################################


# 最大容量

def maxContent2D(weight1s, weight2s, content1, content2, values, nums):
    N = len(weight1s)
    M1 = int(content1)
    M2 = int(content2)
    W = [[0]*(M1+1) for i in range(M2+1)]
    for i in range(N):
        for k in range(nums[i]):
            for j in range(M1,0,-1):
                for p in range(M2,0,-1):
                    if j >= weight1s[i] and p >= weight2s[i]:
                        W[p][j] = max([W[p][j], W[p-weight2s[i]][j-weight1s[i]] + values[i]])
    return W[M2][M1]

# content1 = 10
# content2 = 15
# weight1s = [2,3,1,2]
# weight2s = [3,2,1,4]
# values = [1,5,2,4]
# nums = [1,2,3,2]
# print maxContent2D(weight1s, weight2s, content1, content2, values, nums)



def customMaxContent(weight1s, weight2s, content1, content2, nums):
    N = len(weight1s)
    M1 = int(content1)
    M2 = int(content2)
    W = [[0]*(M1+1) for i in range(M2+1)]
    L = [[{"add":[0]*N} for j in range(M1+1)] for i in range(M2+1)]
    L1 = [0]*N
    for i in range(N):
        for k in range(nums[i]):
            for j in range(M1,-1,-1):
                for p in range(M2,-1,-1):
                    if j >= weight1s[i] and p >= weight2s[i]:
                        if W[p][j] < W[p-weight2s[i]][j-weight1s[i]] + weight2s[i]:
                            L[p][j]["origin"] = (p-weight2s[i],j-weight1s[i])
                            L[p][j]["add"][i] += 1
                        W[p][j] = max([W[p][j], W[p-weight2s[i]][j-weight1s[i]] + weight2s[i]])
    for i in range(M2+1):
        for j in range(M1+1):
            print i,j,L[i][j]
    keyi = M2
    keyj = M1
    for i in range(N-1,-1,-1):
        L1[i] = L[keyi][keyj]["add"][i]
        keyi,keyj = L[keyi][keyj]["origin"]
    return W[M2][M1],L1

content1 = 10
content2 = 15
weight1s = [2,3,1,2]
weight2s = [3,2,1,4]
nums = [1,2,3,3]
print (customMaxContent(weight1s, weight2s, content1, content2, nums))


