from sklearn import neighbors
from sklearn import datasets
from sklearn.cross_validation import train_test_split
from sklearn.metrics import classification_report


data=datasets.load_digits()
print data.data.shape


x_train,x_test,y_train,y_test=train_test_split(data.data,data.target,test_size=0.3,random_state=33)

cf=neighbors.KNeighborsClassifier()

'''
 n_neighbors : int, optional (default = 5)
 |      Number of neighbors to use by default for :meth:`k_neighbors` queries.
 |  
 |  weights : str or callable, optional (default = 'uniform')
 |      weight function used in prediction.  Possible values:
 |  
 |      - 'uniform' : uniform weights.  All points in each neighborhood
 |        are weighted equally.
 |      - 'distance' : weight points by the inverse of their distance.
 |        in this case, closer neighbors of a query point will have a
 |        greater influence than neighbors which are further away.
 |      - [callable] : a user-defined function which accepts an
 |        array of distances, and returns an array of the same shape
 |        containing the weights.
 |  
 |  algorithm : {'auto', 'ball_tree', 'kd_tree', 'brute'}, optional
 |      Algorithm used to compute the nearest neighbors:
 |  
 |      - 'ball_tree' will use :class:`BallTree`
 |      - 'kd_tree' will use :class:`KDTree`
 |      - 'brute' will use a brute-force search.
 |      - 'auto' will attempt to decide the most appropriate algorithm
 |        based on the values passed to :meth:`fit` method.
  |  leaf_size : int, optional (default = 30)
 |      Leaf size passed to BallTree or KDTree.  This can affect the
 |      speed of the construction and query, as well as the memory
 |      required to store the tree.  The optimal value depends on the
 |      nature of the problem.
 |  
 |  metric : string or DistanceMetric object (default = 'minkowski')
 |      the distance metric to use for the tree.  The default metric is
 |      minkowski, and with p=2 is equivalent to the standard Euclidean
 |      metric. See the documentation of the DistanceMetric class for a
 |      list of available metrics.
 |  
 |  p : integer, optional (default = 2)
 |      Power parameter for the Minkowski metric. When p = 1, this is
 |      equivalent to using manhattan_distance (l1), and euclidean_distance
 |      (l2) for p = 2. For arbitrary p, minkowski_distance (l_p) is used.
 |  
 |  metric_params : dict, optional (default = None)
 |      Additional keyword arguments for the metric function.
 |  
 |  n_jobs : int, optional (default = 1)
 |      The number of parallel jobs to run for neighbors search.
 |      If ``-1``, then the number of jobs is set to the number of CPU cores.
 |      Doesn't affect :meth:`fit` method.
'''

cf.fit(x_train,y_train)
y_test_pre=cf.predict(x_test)
y_test_pre_pro=cf.predict_proba(x_test)
score=cf.score(x_test,y_test)
print score
print classification_report(y_test,y_test_pre,target_names=[str(i) for i in data.target_names])
print cf.kneighbors(x_test)
