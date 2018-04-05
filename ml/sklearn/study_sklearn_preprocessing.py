from sklearn import preprocessing
import numpy
a=numpy.random.rand(4,3)*3+1
print a.mean(axis=0)
print a.std(axis=0)
print a.mean()

# scale
a1=preprocessing.scale(a)
print a1.mean(axis=0)
print a1.std(axis=0)


# StandardScaler
s=preprocessing.StandardScaler()
a1=s.fit_transform(a)#a2=sacle(a)
print a1.mean(axis=0)
print s.mean_
print a1.std(axis=0)
print s.std_


# MinMaxScaler
s=preprocessing.MinMaxScaler((0,1))
a1=s.fit_transform(a) # a2=preprocessing.minmax_scale(a)


# MaxAbsScaler
s=preprocessing.MaxAbsScaler()
a1=s.fit_transform(a) # a2=preprocessing.maxabs_scale(a)


# Normalizer
s1=preprocessing.Normalizer('l1')
a1=s1.fit_transform(a)
s2=preprocessing.Normalizer('l2')
a2=s2.fit_transform(a)


# Binarizer
s=preprocessing.Binarizer(0.0)
a1=s.fit_transfrom(a)

# PolynomialFeatures
s=preprocessing.PolynomialFeatures(3)
a1=s.fit_transfrom(s)


# LabelEncoder
s=preprocessing.LabelEncoder()
labels=['big','big','small','media','small','media']
labels1=s.fit_transform(labels)

# MultiLabelBinarizer
s=preprocessing.MultiLabelBinarizer()
labels=[[1,2],[3],[5,6],[1,3],[4,5]]
labels1=s.fit_transform(labels)


