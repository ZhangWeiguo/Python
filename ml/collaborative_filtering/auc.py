# -*- encoding: utf-8 -*-
import numpy
from sklearn import metrics

# 计算两个排序
def auc_score_compare_rank(pro, pre):
    R = {}
    for i,j in pro:
        R[i] = {"pro":j}
    for i,j in pre:
        R[i]["pre"] = j
    N = len(pro)
    if len(pre) != N:
        raise Exception("Error")
    score = 0
    for i in R:
        for j in R:
            if i!=j:
                x = (R[i]["pre"] >= R[j]["pre"])
                y = (R[i]["pro"] >= R[j]["pro"])
                if (x and y) or (not x and not y):
                    score += 1
    return float(score)/(N**2-N)



def cal_result(labels, predicts):
    tp,fp,tn,fn = 0.0,0.0,0.0,0.0
    for i,j in zip(labels, predicts):
        if i == 1 and j == 1:
            tp += 1
        elif i == 1 and j == 0:
            fp += 1
        elif i == 0 and j == 1:
            fn += 1
        elif i == 0 and j == 0:
            tn += 1
    x = fn/(fn+tn)
    y = tp/(tp+fp)
    return x,y

def area(L):
    L.sort(cmp=compare)
    x = [i[0] for i in L]
    y = [i[1] for i in L]
    return numpy.trapz(y, x)

def compare(x,y):
    if x[0] > y[0]:
        return 1
    elif x[0] == y[0]:
        if x[1] > y[1]:
            return 1
        elif x[1] == y[1]:
            return 0
        else:
            return -1
    else:
        return -1


# sklearn 计算 auc
def auc_score_sklearn(labels, predicts):
    f,t,s = metrics.roc_curve(labels, predicts)
    L = [(i,j) for i,j in zip(f,t)]
    score = metrics.auc(f,t)
    # score = metrics.roc_auc_score(labels, predicts)
    return score

# 自定义传统方法计算auc
def auc_score(labels, predicts):
    L = []
    N = max(int(numpy.log(len(labels))),100)
    for i in [1-i*0.1 for i in range(1,N)]:
        p = [0 if j<=i else 1 for j in predicts]
        x,y = cal_result(labels, p)
        L.append((x,y))
    score = area(L)
    return score

# 自定义用rank算auc
def auc_score_rank(labels, predicts):
    M = sum(labels)
    N = len(labels)
    order = numpy.argsort(predicts)
    predicts = [predicts[i] for i in order]
    predicts.reverse()
    labels = [labels[i] for i in order]
    labels.reverse()
    ranks = [(N-i)*1.0 for i in range(N)]
    # same get average
    start,end = 0,0
    for i in range(1,N):
        if predicts[i] == predicts[i-1]:
            end += 1
        else:
            a = sum(ranks[start:end+1])/float(end+1-start)
            for j in range(start,end+1):
                ranks[j] = a
            start, end = i, i
    p_ranksum = sum([ranks[i] if labels[i]==1 else 0 for i in range(N)])
    score = (p_ranksum - M*(M+1)/2.0)/(M*(N-M))
    return score


# for i in range(10):
#     Labels      = numpy.random.randint(0,2,1000)
#     Predicts    = numpy.random.random((1000))
#     print "Custom AUC: %2.4f  Sklearn AUC: %2.4f  Rank AUC: %2.4f"%(
#         auc_score(Labels, Predicts),
#         auc_score_sklearn(Labels, Predicts),
#         auc_score_rank(Labels, Predicts)
#     )
pro = [('a',1),('b',2),('c',3),('d',4)]
pre = [('a',4),('b',5),('c',6),('d',7)]
print auc_score_compare_rank(pro, pre)