# -*- coding: utf-8 -*-
"""
Created on Sat Apr 15 12:44:32 2017

@author: weiguo
"""

from sklearn import datasets
from sklearn.feature_extraction.text import CountVectorizer,TfidfVectorizer
from sklearn.cross_validation import train_test_split
from sklearn.metrics import classification_report,f1_score,precision_score,recall_score
from sklearn import naive_bayes,svm,cluster,neural_network
import time

def learn(learner,x_train,y_train,x_test,y_test):
    learner.fit(x_train,y_train)
    y_pre=learner.predict(x_test)
    score_f1=f1_score(y_test,y_pre,average='weighted')
    score_p=precision_score(y_test,y_pre,average='weighted')
    score_r=recall_score(y_test,y_pre,average='weighted')
    return score_f1,score_p,score_r

news=datasets.fetch_20newsgroups(subset='all')
x=news.data
y=news.target
x_train,x_test,y_train,y_test=train_test_split(x,y)

count=CountVectorizer()
tfidf=TfidfVectorizer()

count1=CountVectorizer(max_features=20000)
tfidf1=TfidfVectorizer(max_features=20000)


count2=CountVectorizer(stop_words='english')
tfidf2=TfidfVectorizer(stop_words='english')


x_train1=count.fit_transform(x_train)
x_test1=count.transform(x_test)

x_train2=tfidf.fit_transform(x_train)
x_test2=tfidf.transform(x_test)

x_train3=count1.fit_transform(x_train)
x_test3=count1.transform(x_test)

x_train4=tfidf1.fit_transform(x_train)
x_test4=tfidf1.transform(x_test)

x_train5=count2.fit_transform(x_train)
x_test5=count2.transform(x_test)

x_train6=tfidf2.fit_transform(x_train)
x_test6=tfidf2.transform(x_test)

#x_train1=x_train1.todense()
#x_train2=x_train2.todense()
#x_test1=x_test1.tode5nse()
#x_test2=x_test2.todense()

cf=[naive_bayes.MultinomialNB(),
    svm.LinearSVC()]

#svm.SVC(),
#neural_network.MLPClassifier(hidden_layer_sizes=(100000,1000000,),max_iter=10000)

name=['Bayes-Multinomaia','SVC-Linear','SVC-RBF','NN-MLP']

print '='*100
print '%-20s%-15s%-10s%-10s%-10s%-10s%-10s%-10s%-5s'%('learner-name','Vec-kind','train-nu',
                                   'test-nu','dimension','precious','recall','f1-score','time')
print '-'*100
(n1,n2)=x_train1.shape
(m1,m2)=x_test1.shape
for learner_name,learner in zip(name,cf):
    t1=time.time()
    score_f1,score_p,score_r=learn(learner,x_train1,y_train,x_test1,y_test)
    t2=time.time()
    print '%-20s%-15s%-10s%-10s%-10s%-10s%-10s%-10s%-5s'%(learner_name,'CountVec',
                                                       str(n1),str(m1),str(n2),
                                                       str(round(score_p,3)),str(round(score_r,3)),
                                                       str(round(score_f1,3)),str(round(t2-t1,3)))
    print '-'*100

(n1,n2)=x_train2.shape
(m1,m2)=x_test2.shape
for learner_name,learner in zip(name,cf):
    t1=time.time()
    score_f1,score_p,score_r=learn(learner,x_train2,y_train,x_test2,y_test)
    t2=time.time()
    print '%-20s%-15s%-10s%-10s%-10s%-10s%-10s%-10s%-5s'%(learner_name,'TfidfVec',
                                           str(n1),str(m1),str(n2),
                                           str(round(score_p,3)),str(round(score_r,3)),
                                           str(round(score_f1,3)),str(round(t2-t1,3)))
    print '-'*100

(n1,n2)=x_train3.shape
(m1,m2)=x_test3.shape
for learner_name,learner in zip(name,cf):
    t1=time.time()
    score_f1,score_p,score_r=learn(learner,x_train3,y_train,x_test3,y_test)
    t2=time.time()
    print '%-20s%-15s%-10s%-10s%-10s%-10s%-10s%-10s%-5s'%(learner_name,'CountVec-limit',
                                           str(n1),str(m1),str(n2),
                                           str(round(score_p,3)),str(round(score_r,3)),
                                           str(round(score_f1,3)),str(round(t2-t1,3)))
    print '-'*100

(n1,n2)=x_train4.shape
(m1,m2)=x_test4.shape
for learner_name,learner in zip(name,cf):
    t1=time.time()
    score_f1,score_p,score_r=learn(learner,x_train4,y_train,x_test4,y_test)
    t2=time.time()
    print '%-20s%-15s%-10s%-10s%-10s%-10s%-10s%-10s%-5s'%(learner_name,'TiidfVec-limit',
                                           str(n1),str(m1),str(n2),
                                           str(round(score_p,3)),str(round(score_r,3)),
                                           str(round(score_f1,3)),str(round(t2-t1,3)))
    print '-'*100


(n1,n2)=x_train5.shape
(m1,m2)=x_test5.shape
for learner_name,learner in zip(name,cf):
    t1=time.time()
    score_f1,score_p,score_r=learn(learner,x_train5,y_train,x_test5,y_test)
    t2=time.time()
    print '%-20s%-15s%-10s%-10s%-10s%-10s%-10s%-10s%-5s'%(learner_name,'CountVec-stop',
                                           str(n1),str(m1),str(n2),
                                           str(round(score_p,3)),str(round(score_r,3)),
                                           str(round(score_f1,3)),str(round(t2-t1,3)))
    print '-'*100

(n1,n2)=x_train6.shape
(m1,m2)=x_test6.shape
for learner_name,learner in zip(name,cf):
    t1=time.time()
    score_f1,score_p,score_r=learn(learner,x_train6,y_train,x_test6,y_test)
    t2=time.time()
    print '%-20s%-15s%-10s%-10s%-10s%-10s%-10s%-10s%-5s'%(learner_name,'TiidfVec-stop',
                                           str(n1),str(m1),str(n2),
                                           str(round(score_p,3)),str(round(score_r,3)),
                                           str(round(score_f1,3)),str(round(t2-t1,3)))
    print '-'*100



print '='*100