# -*- encoding:utf-8 -*-

from gensim import models
'''
tf-idf = tf * idf
tf 词频
idf 总样本数/有该词的样本数


 #corpus： 语料
 #id2word： id转向词函数
 #dictionary：词典
 #wlocal: 用在计算
 #      vector = [(termid, self.wlocal(tf) 
 # self.idfs.get(termid))
 #         for termid, tf in bow if self.idfs.get(termid, 0.0) != 0.0] 
# wglobal: 用要计算地方
#              dict((termid, wglobal(df, total_docs))
#            for termid, df in iteritems(dfs))
# normalize: 规范化处理；这个可以是一个布尔类型的值，也可以是自定义的函数,True用欧几里得模


weight_{i,j} = frequency_{i,j} * log_2(D / document_freq_{i})
weight_{i,j} = wlocal(frequency_{i,j}) * wglobal(document_freq_{i}, D)

'''
corpus = \
        [[(0, 1.0), (1, 1.0), (2, 1.0)],
        [(2, 1.0), (3, 1.0), (4, 1.0), (5, 1.0), (6, 1.0), (8, 1.0)],
        [(1, 1.0), (3, 1.0), (4, 1.0), (7, 1.0)],
        [(0, 1.0), (4, 2.0), (7, 1.0)],
        [(3, 1.0), (5, 1.0), (6, 1.0)],
        [(9, 1.0)],
        [(9, 1.0), (10, 1.0)],
        [(9, 1.0), (10, 1.0), (11, 1.0)],
        [(8, 1.0), (10, 1.0), (11, 1.0)]]
tfidf = models.TfidfModel(corpus, normalize=True)
vec = [(0, 1), (4, 1)]
print(tfidf[vec])
vec = [(0, 2), (4, 1)]
print(tfidf[vec])