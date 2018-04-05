# -*-encoding:utf-8-*-
import numpy
from sklearn import datasets
from gensim.models import Word2Vec


class get_sentence:
    def __init__(self,N):
        data = datasets.fetch_20newsgroups()
        self.data = data.data
        self.length = len(data)
        self.max_num = N
        self.current_num = 0
    def __iter__(self):
        return self
    def next(self):
        i = numpy.random.randint(0,self.length)
        self.current_num+=16
        if self.max_num <= self.current_num:
            raise  StopIteration
        else:
            L = self.data[i].replace("\n",' ').lower().split(" ")
            LL = [i for i in L if "'" not in i and "(" not in i and ")" not in i and "-" not in i and "_" not in i]
            return LL

data = datasets.fetch_20newsgroups()
docs = data.data
type = data.target
type_name = data.target_names
sentences = get_sentence(len(docs))
Model = Word2Vec(size=100)
Model.build_vocab(sentences)
Model.train(sentences,total_examples=Model.corpus_count,epochs=Model.iter)
Model.save("word2vec")
print Model.similar_by_word("guns")
print Model.wv['you']
M1 = Word2Vec.load("word2vec")
