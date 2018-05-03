# -*-encoding:utf-8-*-
import numpy,json,urllib2
from sklearn.cluster import KMeans

def test():
    f = file("video_tag", 'r')
    tag = {}
    s = f.read().split("\n")
    for i in s:
        p = i.split(",")
        if len(p) >= 2:
            if "meaningless" in p[1]:
                p[1] = "meaningless"
            tag[p[0]] = p[1]

    Data = []
    n_clusters = 5
    f = file("video_vector",'r')
    while True:
        s = f.readline()
        if not s:
            break
        s = s.replace("\n","")
        J = json.loads(s)
        Data.append(J['data'])
    f.close()
    Data = numpy.array(Data)
    Model = KMeans(n_clusters=n_clusters)
    Model.fit_transform(Data)

    F = []
    for i in range(n_clusters):
        f1 = file("video_cluster%d.html"%i, 'w')
        f1.write("<html><body>\n")
        F.append(f1)
    f = file("video_vector", 'r')
    while True:
        s = f.readline()
        if not s:
            break
        s = s.replace("\n","")
        J = json.loads(s)
        image_url =  "http://100.84.73.160:3000/id/cover?id=" + str(J["id"])
        response = urllib2.urlopen(image_url)
        real_url = response.read()
        key = J['id']
        if key in tag:
            video_tag = tag[key]
        else:
            video_tag = "Unknow"
        s1 = '''<img src = "%s" width="100">%s\n''' % (real_url,video_tag)
        k = Model.predict(numpy.array(J['data']).reshape(1,-1))[0]
        F[k].write(s1)
    for i in range(n_clusters):
        F[i].write("</body></html>")
        F[i].close()


test()