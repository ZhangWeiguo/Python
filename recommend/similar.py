# -*-encoding:utf-8-*-
from svd import SVD as SVD1
from svd_advance import SVD as SVD2
from svd_direct import SVD as SVD
import numpy,json
import urllib2
from conf import conf

def test(video_id):
    f = file("video_tag", 'r')
    tag = {}
    s = f.read().split("\n")
    for i in s:
        p = i.split(",")
        if len(p) >= 2:
            if "meaningless" in p[1]:
                p[1] = "meaningless"
            tag[p[0]] = p[1]

    Model = SVD(conf["n_dimsion"])
    f = file("video_vector",'r')
    while True:
        s = f.readline()
        if not s:
            break
        s = s.replace("\n","")
        J = json.loads(s)
        Model.item_vector[J["id"]] = numpy.array(J["data"])
    f.close()
    similar_videos, similarity = Model.similar_items(video_id, num=100, distname='cosine')
    f = file("test.html", 'w')
    f.write("<html><body>\n")
    similar_videos.insert(0,video_id)
    similarity.insert(0,1)
    for key, value in zip(similar_videos, similarity):
        image_url =  "http://100.84.73.160:3000/id/cover?id=" + str(key)
        print image_url
        response = urllib2.urlopen(image_url)
        real_url = response.read()
        if key in tag:
            video_tag = tag[key]
        else:
            video_tag = "Unknow"
        s1 = '''<img src = "%s" width="100"> %f\n%s\n''' % (real_url, value,video_tag)
        f.write(s1)
    f.write("</body></html>")

test("a0nnfu66qqj")