from gensim import corpora

L = ["I am a dog","I am a cat , and you are dog","I am not a dog but a cat"]
stop_words = ["I",","]

L = [i.split() for i in L]
D = corpora.Dictionary()
D.add_documents(L)          # add docs
D.filter_tokens(bad_ids = [D.token2id[i] for i in stop_words], good_ids = None)
D.compactify()              # reomve the gaps, in fact it did as automicly
print D.id2token            # dict(id) = token
print D.token2id            # dict(token) = id
print D.dfs                 # dict(token) = freq
for doc in L:
    print D.doc2bow(doc)


corpus = [D.doc2bow(doc) for doc in L]
corpora.MmCorpus.serialize('corpus.mm', corpus)
corpora.SvmLightCorpus.serialize('corpus.svmlight', corpus)
corpora.BleiCorpus.serialize('corpus.lda-c', corpus)
corpora.LowCorpus.serialize('corpus.low', corpus)

corpus = corpora.MmCorpus('corpus.mm')
corpus = corpora.SvmLightCorpus('corpus.svmlight')
corpus = corpora.BleiCorpus('corpus.lda-c')
corpus = corpora.LowCorpus('corpus.low')