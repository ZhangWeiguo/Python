# -*-encoding:utf-8-*-
import numpy,random,json
from conf import score_dict

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

    def train_iter(self,data_iter, N):
        for k in range(N):
            kk = 0
            print "begin the %dth training" % k
            for s in data_iter:
                kk += 1
                L = s.split(",")
                if len(L) == 3:
                    user_id = L[0]
                    video_id = L[1]
                    action = L[2].replace("\n", "")
                    if len(user_id) >= 10 and len(video_id) >= 10:
                        self.train(user_id, video_id, action)
            print "end the %dth training" % k

    def train_file(self,filename, N):
        f = file(filename, 'r')
        all_data = f.read().split("\n")
        order = range(len(all_data))
        f.close()
        for k in range(N):
            random.shuffle(order)
            kk = 0
            print "begin the %dth training" % k
            for i in order:
                s = all_data[i]
                kk += 1
                L = s.split(",")
                if len(L) == 3:
                    user_id = L[0]
                    video_id = L[1]
                    action = L[2].replace("\n", "")
                    if len(user_id) >= 10 and len(video_id) >= 10:
                        self.train(user_id, video_id, action)
            print "end the %dth training" % k

    def train(self,user_id,item_id,action):
        self.train_nums += 1
        self.step = self.init_step*(self.step_decay[0]**(float(self.train_nums)/self.step_decay[1]))
        if action in self.score_dict.keys():
            data = self.score_dict[action]
        else:
            data = 0.0
        if user_id in self.user_vector:
            user_exist = True
        else:
            user_exist = False
            self.user_vector[user_id] = numpy.random.rand(self.n_dimsion)
            self.user_vector[user_id] = 1 * self.user_vector[user_id] / numpy.sqrt(numpy.sum(self.user_vector[user_id] ** 2))
        if item_id in self.item_vector:
            item_exist = True
        else:
            item_exist = False
            self.item_vector[item_id] = numpy.random.rand(self.n_dimsion)
            self.item_vector[item_id] = 1 * self.item_vector[item_id] / numpy.sqrt(numpy.sum(self.item_vector[item_id] ** 2))

        if self.train_nums % 10000 == 0:
            error1,error2 = self.error(user_id, item_id, action)
            print "%10d action=%15s realerror=%8.4f allerror=%8.4f step=%5.4f key=%5.2f,%5.2f" \
                  % (self.train_nums, action, error1, error2, self.step,
                     numpy.sqrt(numpy.sum(self.item_vector[item_id] ** 2)),
                     numpy.sqrt(numpy.sum(self.user_vector[user_id] ** 2)))

        if (not item_exist) and user_exist:
            self.user_vector[user_id],self.item_vector[item_id] = \
            self.sd(user_v = self.user_vector[user_id],
                    item_v = self.item_vector[item_id],
                    data = data,
                    user_step = 0.0,
                    item_step = self.step,
                    alpha1=self.alpha1,
                    alpha2=self.alpha2)
        if (not user_exist) and item_exist:
            self.user_vector[user_id], self.item_vector[item_id] = \
            self.sd( user_v=self.user_vector[user_id],
                     item_v=self.item_vector[item_id],
                     data=data,
                     user_step=self.step,
                     item_step=0.0,
                     alpha1=self.alpha1,
                     alpha2=self.alpha2)
        if ((not item_exist) and (not user_exist)) or (item_exist and user_exist):
            self.user_vector[user_id], self.item_vector[item_id] = \
                self.sd(user_v = self.user_vector[user_id],
                         item_v=self.item_vector[item_id],
                         data=data,
                         user_step=self.step,
                         item_step=self.step,
                         alpha1=self.alpha1,
                         alpha2=self.alpha2)
        if self.train_nums % 10000 == 0:
            error1,error2 = self.error(user_id, item_id, action)
            print "%10d action=%15s realerror=%8.4f allerror=%8.4f step=%5.4f key=%5.2f,%5.2f" \
                  % (self.train_nums, action, error1, error2, self.step,
                     numpy.sqrt(numpy.sum(self.item_vector[item_id] ** 2)),
                     numpy.sqrt(numpy.sum(self.user_vector[user_id] ** 2)))

    def sd(self,user_v,item_v,data,user_step,item_step,alpha1,alpha2):
        x = numpy.dot(user_v.reshape((-1, 1)), (item_v).reshape(1, -1))[0, 0]

        # du = -4.0 * (data - numpy.square(x)) * x * item_v + \
        #      4.0 * alpha1 * (numpy.sum(numpy.square(user_v)) - 1) * user_v
        # di = -4.0 * (data - numpy.square(x)) * x * user_v + \
        #      4.0 * alpha2 * (numpy.sum(numpy.square(item_v)) - 1) * item_v
        du = -2.0 * (data - numpy.square(x)) * x * item_v
        di = -2.0 * (data - numpy.square(x)) * x * user_v

        du = numpy.minimum(numpy.maximum( du , -1e10),1e3)
        di = numpy.minimum(numpy.maximum( di , -1e10),1e3)
        user_v -= user_step * du
        item_v -= item_step * di
        return user_v,item_v

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





