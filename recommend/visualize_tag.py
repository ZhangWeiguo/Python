# -*-encoding:utf-8-*-
from sklearn.manifold import TSNE
from sklearn.linear_model import LogisticRegression
from sklearn.decomposition import PCA,TruncatedSVD
from sklearn.cross_validation import train_test_split
from sklearn.metrics import confusion_matrix
import numpy,json
from matplotlib import pyplot

f = file("video_tag",'r')
tag = {}
tag_num = {}
tag_pair = {}
s = f.read().split("\n")
for i in s:
    p = i.split(",")
    if len(p) >= 2:
        if "man_meaningless" in p[1]:
            p[1] = "man_meaningless"
        tag[p[0]] = p[1]
        if p[1] in tag_num:
            tag_num[p[1]] +=1
        else:
            tag_num[p[1]] = 1
    else:
        print i
k = 0
for i in tag_num:
    tag_pair[i] = k
    k += 1
    print "%-20s:%d"%(i,tag_num[i])

Data = []
Target = []
f = file("video_vector", 'r')
while True:
    s = f.readline()
    if not s:
        break
    s = s.replace("\n", "")
    J = json.loads(s)
    if J["id"] in tag:
        Data.append(J["data"])
        Target.append(tag_pair[tag[J["id"]]])
f.close()
Data = numpy.array(Data)
Target = numpy.array(Target).reshape((-1,1))
print "All samples shape: ",Data.shape

# T = TSNE(n_components=2)
# Data_2 = T.fit_transform(Data)
#
P =TruncatedSVD(n_components=2)
Data_2 = P.fit_transform(Data)
# print P.score(Data)
pyplot.scatter(Data_2[:,0],Data_2[:,1],c=Target)
pyplot.show()

# Data_train,Data_test,Target_train,Target_test = train_test_split(Data,Target)
# L = LogisticRegression()
# L.fit(Data_train,Target_train)
# print L.score(Data_train,Target_train)
# print L.score(Data_test,Target_test)

# print confusion_matrix(Target,L.predict(Data))