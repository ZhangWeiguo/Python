# -*-encoding:utf-8 -*-
'''
created by zwg in 2017-04-26
'''

from sklearn import feature_extraction,feature_selection
from sklearn import datasets
from sklearn.cross_validation import train_test_split
from sklearn import tree

'''
For regression: f_regression, mutual_info_regression
For classification: chi2, f_classif, mutual_info_classif
'''


data=datasets.load_breast_cancer()
X=data.data
Y=data.target

# 卡方检验
Select11=feature_selection.SelectKBest(feature_selection.chi2,k=5)
X11=Select11.fit_transform(X,Y)
print Select11.scores_


Select12=feature_selection.SelectPercentile(feature_selection.chi2,precentile=30)
X12=Select12.fit_transform(X,Y)
print Select12.scores_

# 方差
Select2=feature_selection.VarianceThreshold(5)
X2=Select2.fit_transform(X,Y)
print Select2.variances_

# 互信息
Select3=feature_selection.SelectKBest(feature_selection.mutual_info_classif,k=10)
X3=Select3.fit_transform(X,Y)
print Select3.scores_

# 方差分析
Select4=feature_selection.SelectKBest(feature_selection.f_classif,k=10)
X4=Select4.fit_transform(X,Y)
print Select4.scores_


# 依据模型






