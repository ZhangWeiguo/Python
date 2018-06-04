import numpy

Labels      = [0, 1, 1, 0, 1, 1, 0, 0]
Predicts    = [0.1, 0.7, 0.8, 0.3, 0.9, 0.8, 0.1, 0.9]

# from sklearn import metrics
# print metrics.roc_auc_score(Labels, Predicts)


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




def auc_score(labels, predicts):
    L = []
    for i in [1-i*0.1 for i in range(1,10)]:
        p = [0 if j<=i else 1 for j in predicts]
        x,y = cal_result(labels, p)
        L.append((x,y))
    print L
    score = 0
    for k,i in enumerate(L):
        x,y = i
        if k == 0:
            score += y*x
        else:
            score += y*(x-L[k-1][0])
    return score


print auc_score(Labels, Predicts)