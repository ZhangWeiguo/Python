# -*- coding: utf-8 -*-
# created by zwg in 20180617
from token_access import TokenAccess
import urllib2
import poster.encode
from poster.streaminghttp import register_openers

class Media(object):
    def __init__(self):
        register_openers()
    #上传图片
    def uplaod(self, access_token, filepath, media_type):
        openFile = open(filePath, "rb")
        param = {'media': openFile}
        post_data, post_headers = poster.encode.multipart_encode(param)
        post_url = "https://api.weixin.qq.com/cgi-bin/media/upload?access_token=%s&type=%s" %(access_token, media_type)
        request = urllib2.Request(post_url, post_data, post_headers)
        urlResp = urllib2.urlopen(request)
        print urlResp.read()

if __name__ == '__main__':
    myMedia = Media()
    access_token = TokenAccess.get_access_token()
    file_path = "../static/test.jpg"
    media_type = "image"
    open_file = open(file_path, "rb")
    param= {'media': open_file}
    post_data, post_headers = poster.encode.multipart_encode(param)
    print post_headers
    print post_data
    myMedia.uplaod(access_token, file_path, media_type)