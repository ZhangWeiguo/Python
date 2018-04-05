# -*-encoding:utf8-*-
'''
created by zwg
'''

import numpy,shelve,os
import time,urllib2,json,hashlib,urllib
import threadpool

class WaApi():
    def __init__(self):
        self.table_url = 'https://api-in-wa.uc.cn/api/queryStatKeyCode'
        self.log_url = 'http://tunnel.in.wa.uc.local:22310/tunnel/get_log'
        self.keyCode = "a9603ba96edd426eb47596f158eb579e"
        self.secretKey = "87986d6717c34c16b34c58289feeea73"
        self.app = "30001"
        P = {}
        statKey = "16727"
        statId = "16727_dim_1"
        P['app'] = self.app
        P['statKey'] = statKey
        P['statId'] = statId
        s = P['app'] + P['statKey'] + P['from'] + P['to'] + str(P['tm']) + self.secretKey + self.keyCode
        P['sign'] = sign = hashlib.md5(s).hexdigest()
        P['needOriginDimValue'] = "false"
        P['keyCode'] = self.keyCode
        self.P = P

    def Get(video_id,country = "IN",dt = "2017-12-04"):
        begin = "%s 00:00"%dt
        end = "%s 00:00"%dt
        dataFilters = '[{"field": "video_id", "operator": "str_eq_ignorecase", "value": "%s"},\
                            {"field": "country", "operator": "str_eq_ignorecase", "value": "%s"}]'%(video_id,country)
        self.P["dataFilters"] = dataFilters
        self.P['tm'] = long(time.time()) * 1000
        self.P['from'] = begin
        self.P['to'] = end
        request = urllib2.Request(url=self.table_url, data=urllib.urlencode(P))
        page = urllib2.urlopen(request)
        result = page.read()
        R = json.loads(result)
        return R


class RecommendNet():
    def __init__(self):
        self.users = {}
        self.items = {}
        self.items_inv = {}
        self.users_items = {}
        self.items_users = {}
        self.items_similarity = None
        self.alpha = 2

    def CollectData(self,data):
        k_i = 0
        k_u = 0
        for user,item,weight in data:
            if user not in self.users:
                self.users[user] = k_u
                self.users_items[k_u] = set()
                k_u += 1
            if item not in self.items:
                self.items[item] = k_i
                self.items_users[k_i] = set()
                k_i += 1
            self.users_items[self.users[user]].add(self.items[item])
            self.items_users[self.items[item]].add(self.users[user])

        for key in self.items:
            self.items_inv[self.items[key]] = key


    def sim(self,item1,item2,kind):
        alpha = self.alpha
        s = 0.0
        if kind == "Adamic":
            commen_users = self.items_users[item1].intersection(self.items_users[item2])
            for user in commen_users:
                s += 1.0/numpy.log(2+len(self.users_items[user]))
        elif kind == "Swing":
            commen_users = self.items_users[item1].intersection(self.items_users[item2])
            for user1 in commen_users:
                for user2 in commen_users:
                    if user1 != user2:
                        s += 1.0/(alpha+len(self.users_items[user1].intersection(self.users_items[user2])))   
        elif kind == "Sim":
            commen_users = self.items_users[item1].intersection(self.items_users[item2])
            for user1 in commen_users:
                for user2 in commen_users:
                    if user1 != user2:
                        x = len(self.users_items[user1].intersection(self.users_items[user2]))
                        s += numpy.log(alpha + x)
            nn = len(self.items_users[item1].union(self.items_users[item2]))
            s = s/numpy.log(alpha+nn)
        if s != 0:
            print s
        self.items_similarity[item1,item2] = s
        self.items_similarity[item2,item1] = s

    def AdamicItems(self):
        N = len(self.items)
        self.items_similarity = numpy.zeros((N,N))
        pool = threadpool.ThreadPool(100)
        for item1 in self.items_users:
            for item2 in self.items_users:
                if item1 >= item2:
                    if item1 == item2:
                        self.items_similarity[item1,item2] = 1e20
                    continue
                requests = threadpool.makeRequests(self.sim, [((item1,item2,),{'kind':'Sim'})])
                [pool.putRequest(request) for request in requests]
        pool.wait()


    def SwingItems(self, alpha):
        self.alpha = alpha
        N = len(self.items)
        self.items_similarity = numpy.zeros((N,N))
        pool = threadpool.ThreadPool(100)
        for item1 in self.items_users:
            for item2 in self.items_users:
                if item1 >= item2:
                    if item1 == item2:
                        self.items_similarity[item1,item2] = 1e20
                    continue
                requests = threadpool.makeRequests(self.sim, [((item1,item2,),{'kind':'Swing'})])
                [pool.putRequest(request) for request in requests]
        pool.wait()


    def SimItems(self, alpha):
        self.alpha = alpha
        N = len(self.items)
        self.items_similarity = numpy.zeros((N,N))
        pool = threadpool.ThreadPool(100)
        for item1 in self.items_users:
            for item2 in self.items_users:
                if item1 >= item2:
                    if item1 == item2:
                        self.items_similarity[item1,item2] = 1e20
                    continue
                requests = threadpool.makeRequests(self.sim, [((item1,item2,),{'kind':'Sim'})])
                [pool.putRequest(request) for request in requests]
        pool.wait()

    def RecommendByItem(self,item, num = 100):
        items = []
        values = []
        if item in self.items:
            id = self.items[item]
        else:
            return items,values

        items = range(len(self.items))
        values = self.items_similarity[id,:]
        order = list(numpy.argsort(values))
        order.reverse()
        items = [items[i] for i in order]
        values = [values[i] for i in order]
        N = len(items)
        if N >= num:
            items = items[0:num]
            values = values[0:num]
        items = [self.items_inv[i] for i in items ]
        return items,values



    def Save(self,filename):
        if os.path.exists(filename):
            pass
        else:
            os.mkdir(filename)

        f = file(os.path.join(filename,"users"),'w')
        for i in self.users:
            f.write("%s::%s\n"%(i,self.users[i]))
        f.close()

        f = file(os.path.join(filename,"items"),'w')
        for i in self.items:
            f.write("%s::%s\n"%(i,self.items[i]))
        f.close()

        f = file(os.path.join(filename,"items_inv"),'w')
        for i in self.items_inv:
            f.write("%s::%s\n"%(i,self.items_inv[i]))
        f.close()

        f = file(os.path.join(filename,"users_items"),'w')
        for i in self.users_items:
            f.write("%s::%s\n"%(i,json.dumps(list(self.users_items[i]))))
        f.close()

        f = file(os.path.join(filename,"items_users"),'w')
        for i in self.items_users:
            f.write("%s::%s\n"%(i,json.dumps(list(self.items_users[i]))))
        f.close()

        numpy.save(os.path.join(filename,'items_similarity.npy'),self.items_similarity)


    def Restore(self,filename):
        f = file(os.path.join(filename,"users"),'r')
        s = f.readline()
        while s:
            s = s.replace('\n','')
            i,j = s.split("::")
            self.users[i] = j
            s = f.readline()
        f.close()

        f = file(os.path.join(filename,"items"),'r')
        while s:
            s = s.replace('\n','')
            i,j = s.split("::")
            self.items[i] = j
            s = f.readline()
        f.close()

        f = file(os.path.join(filename,"items_inv"),'r')
        while s:
            s = s.replace('\n','')
            i,j = s.split("::")
            self.items_inv[i] = j
            s = f.readline()
        f.close()

        f = file(os.path.join(filename,"users_items"),'r')
        while s:
            s = s.replace('\n','')
            i,j = s.split("::")
            self.users_items[i] = set(json.loads(j))
            s = f.readline()
        f.close()


        f = file(os.path.join(filename,"items_users"),'r')
        while s:
            s = s.replace('\n','')
            i,j = s.split("::")
            self.items_users[i] = set(json.loads(j))
            s = f.readline()
        f.close()


        self.items_similarity = numpy.load(os.path.join(filename,'items_similarity.npy'))




def train(kind, filename):
    from conf import score_dict
    f = file("action_train.log", 'r')
    all_data = f.read().split("\n")
    order = range(len(all_data))
    f.close()
    data = []

    for i in order:
        s = all_data[i]
        L = s.split(",")
        if len(L) == 3:
            user_id = L[0]
            item_id = L[1]
            action = L[2]
            if len(user_id) >= 10 and len(item_id) >= 10:
                if score_dict[action] >= 1:
                    data.append([user_id,item_id,score_dict[action]])

    

    print "Begin to Collect data"
    N.CollectData(data)
    print "End to Collect data"

    print "Begin to Cal Similarity"
    if kind == "Swing":
        N.SwingItems(alpha=2)
    elif kind == "Sim":
        N.SimItems(alpha=2)
    elif kind == "Adamic":
        N.AdamicItems()

    print "End to Cal Similarity"

    print "Begin to Save"
    N.Save(filename)
    print "End to Save"

    # print "Begin to Restore"
    # N.Restore("Net.dat")
    # print "End to Restore"


def test(video_id, filename):
    items,values = N.RecommendByItem(video_id,100)
    f = file("video_tag", 'r')
    tag = {}
    s = f.read().split("\n")
    for i in s:
        p = i.split(",")
        if len(p) >= 2:
            if "meaningless" in p[1]:
                p[1] = "meaningless"
            tag[p[0]] = p[1]


    similar_videos, similarity = items, values
    f = file(filename, 'w')
    f.write('''<html><body><table border="1" align="center" width="1000"> <tr><th width="40%">Image</th>
        <th width="15%">id</th><th width="15%">score</th><th width="15%">tag</th><th width="15%">edges</th></tr>\n''')
    try:
        for key, value in zip(similar_videos, similarity):
            image_url =  "http://100.84.73.160:3000/id/cover?id=" + str(key)
            print image_url
            response = urllib2.urlopen(image_url)
            real_url = response.read()
            if key in tag:
                video_tag = tag[key]
            else:
                video_tag = "Unknow"
            edges = len(N.items_users[N.items[key]])
            f.write("<tr>\n")
            f.write('''<td><img src = "%s" width="100"></td>\n''' % (real_url))
            f.write('''<td>%s</td><td>%f</td><td>%s</td><td>%d</td>''' % (key,value,video_tag,edges))
            f.write("</tr>\n")
    except:
        pass
    f.write("</tr></table></body></html>")
    f.close()




N = RecommendNet()

train("Adamic","AdamicNet.dat")
test("ava17b6p1ku","test_hot_adamic.html")
test("ava1vde8zxu","test_cold_adamic.html")

train("Swing","SwingNet.dat")
test("ava17b6p1ku","test_hot_swing.html")
test("ava1vde8zxu","test_cold_swing.html")

train("Sim","SimNet.dat")
test("ava17b6p1ku","test_hot_sim.html")
test("ava1vde8zxu","test_cold_sim.html")