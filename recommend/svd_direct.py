# -*-encoding:utf-8-*-
import numpy,random,json
from scipy.sparse import csr_matrix,csc_matrix
from sklearn.decomposition import TruncatedSVD
from conf import score_dict
from numpy.linalg import svd

class SVD:
    def __init__(self,
                 n_dimsion=100,
                 init_step=0.1,
                 step_decay=(1.0,100.0),
                 alpha1=0.0001,
                 alpha2=0.0001):
        self.n_dimsion = n_dimsion
        self.step = init_step
        self.init_step = init_step
        self.alpha1 = alpha1
        self.alpha2 = alpha2
        self.step_decay = step_decay
        self.train_nums = 0
        self.user_vector = {}
        self.item_vector = {}
        self.score_dict = score_dict
        self.dist = {}
        self.dist['cosine'] = lambda x, y: numpy.dot(x.reshape((1, -1)), y.reshape((-1, 1)))[0, 0] / \
                                      (numpy.sqrt(numpy.sum(x ** 2)) *
                                       numpy.sqrt(numpy.sum(y ** 2)))
        self.dist['euclidean'] = lambda x, y: numpy.sqrt(numpy.sum((x - y) ** 2))



    def train_file(self,filename, N):
        f = file(filename, 'r')
        all_data = f.read().split("\n")
        order = range(len(all_data))
        f.close()
        all_users = {}
        all_users_view_num = {}
        all_videos = {}

        for i in order:
            s = all_data[i]
            L = s.split(",")
            if len(L) == 3:
                user_id = L[0]
                video_id = L[1]
                action = L[2].replace("\n", "")
                if len(user_id) >= 10 and len(video_id) >= 10:
                    if not user_id in all_users:
                        all_users[user_id] = len(all_users)
                        all_users_view_num[user_id] = 1
                    else:
                        all_users_view_num[user_id] += 1
                    if not video_id in all_videos:
                        all_videos[video_id] = len(all_videos)
        n0 = len(all_users)
        n1 = len(all_videos)
        print n0, n1

        row = []
        col = []
        d = []
        for i in order:
            s = all_data[i]
            L = s.split(",")
            if len(L) == 3:
                user_id = L[0]
                video_id = L[1]
                action = L[2].replace("\n", "")
                if len(user_id) >= 10 and len(video_id) >= 10:
                    x = all_users[user_id]
                    y = all_videos[video_id]
                    row.append(x)
                    col.append(y)
                    d.append(self.score_dict[action])

        score_matrix = csc_matrix((d,(col, row)),shape=(n1, n0))
        T = TruncatedSVD(n_components=100)
        embeding_matrix = T.fit_transform(score_matrix)
        for i in all_videos:
            x = all_videos[i]
            self.item_vector[i] = embeding_matrix[x,:]
        print numpy.mean(score_matrix)









    def predict(self,user_id,item_id):
        if user_id in self.user_vector:
            if item_id in self.item_vector:
                x = numpy.dot(self.user_vector[user_id].reshape((-1, 1)),
                              (self.item_vector[item_id]).reshape(1, -1))[0, 0]
                return x
        return -1.0

    def error(self,user_id,item_id,action):
        x = self.predict(user_id,item_id)
        error1 = numpy.abs(self.score_dict[action] - x)
        error2 = error1**2 + self.alpha1 * numpy.sum(self.user_vector[user_id]**2) + self.alpha2 * numpy.sum(self.item_vector[item_id]**2)
        return error1,error2

    def recommend_items(self,user_id,num = 100):
        items = []
        values = []
        if user_id in self.user_vector:
            u = self.user_vector[user_id]
            for video in self.item_vector:
                items.append(video)
                values.append(self.predict(user_id,video))
            order = list(numpy.argsort(values))
            order.reverse()
            items = [items[i] for i in order]
            values = [values[i] for i in order]
            N = len(items)
            if N >= num:
                items = items[0:num]
                values = values[0:num]
        return items

    def similar_items(self,item_id,num = 100,distname = 'cosine'):
        items = []
        similarity = []
        N = 0
        if item_id in self.item_vector:
            data = self.item_vector[item_id]
            for item in self.item_vector.keys():
                if item != item_id:
                    N += 1
                    data1 = self.item_vector[item]
                    if numpy.sum(data1**2) > 0 :
                        items.append(item)
                        similarity.append(self.dist[distname](data,data1))
            order = list(numpy.argsort(similarity))
            order.reverse()
            items = [items[i] for i in order]
            similarity = [similarity[i] for i in order]
            if N >= num:
                items = items[0:num]
                similarity = similarity[0:num]
        return items,similarity
    def save(self,user_filename,item_filename):
        f = file(item_filename, 'w')
        for video in self.item_vector:
            d = {}
            d['id'] = video
            d['data'] = list(self.item_vector[video])
            f.write("%s\n" % (json.dumps(d)))
        f.close()

        f = file(user_filename, 'w')
        for user in self.user_vector:
            d = {}
            d['id'] = user
            d['data'] = list(self.user_vector[user])
            f.write("%s\n" % (json.dumps(d)))
        f.close()

    def restore(self,user_filename,item_filename):
        f = file(item_filename, 'r')
        while True:
            s = f.readline()
            if not s:
                break
            s = s.replace("\n", "")
            J = json.loads(s)
            self.item_vector[J["id"]] = numpy.array(J["data"])
        f.close()
        f = file(user_filename, 'r')
        while True:
            s = f.readline()
            if not s:
                break
            s = s.replace("\n", "")
            J = json.loads(s)
            self.user_vector[J["id"]] = numpy.array(J["data"])
        f.close()





