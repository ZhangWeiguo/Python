import numpy
from sklearn import metrics





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
    score = 0
    for k,i in enumerate(L):
        x,y = i
        if k == 0:
            score += y*x
        else:
            score += y*(x-L[k-1][0])
    return score

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


def auc_score_sklearn(labels, predicts):
    f,t,s = metrics.roc_curve(labels, predicts)
    L = [(i,j) for i,j in zip(f,t)]
    # print L
    score = metrics.auc(f,t)
    # score = metrics.roc_auc_score(labels, predicts)
    return score

def auc_score(labels, predicts):
    L = []
    for i in [1-i*0.1 for i in range(1,10)]:
        p = [0 if j<=i else 1 for j in predicts]
        x,y = cal_result(labels, p)
        L.append((x,y))
    L = list(set(L))
    L.sort(cmp=compare)
    # print L
    score = area(L)
    return score

for i in range(10):
    Labels      = numpy.random.randint(0,2,1000)
    Predicts    = numpy.random.random((1000))
    print "Custom AUC: ", auc_score(Labels, Predicts)
    print "Sklean AUC: ", auc_score_sklearn(Labels, Predicts)
