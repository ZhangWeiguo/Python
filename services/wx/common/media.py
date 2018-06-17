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
    def uplaod(self, access_token, file_path, media_type):
        open_file = open(file_path, "rb")
        param = {'media': open_file}
        post_data, post_headers = poster.encode.multipart_encode(param)
        post_url = "https://api.weixin.qq.com/cgi-bin/media/upload?access_token=%s&type=%s" %(access_token, media_type)
        request = urllib2.Request(post_url, post_data, post_headers)
        url_resp = urllib2.urlopen(request)
        return url_resp.read()
    
    def download(self, access_token, media_id, media_path):
        post_url = "https://api.weixin.qq.com/cgi-bin/media/get?access_token=%s&media_id=%s" % (access_token, media_id)
        url_resp = urllib2.urlopen(post_url)

        headers = url_resp.info().__dict__['headers']
        if ('Content-Type: application/json\r\n' in headers) or ('Content-Type: text/plain\r\n' in headers):
            json_dict = json.loads(url_resp.read())
        else:
            buffer = url_resp.read()
            media_file = file(media_path, "wb")
            media_file.write(buffer)
    
    def upload_forever_media(self, access_token, file_path, media_type):
        # 除了视频之外的文件
        open_file = open(file_path, "rb")
        param = {'media': open_file}
        post_data, post_headers = poster.encode.multipart_encode(param)
        post_url = "https://api.weixin.qq.com/cgi-bin/material/add_material?access_token=%s&type=%s" %(access_token, media_type)
        request = urllib2.Request(post_url, post_data, post_headers)
        url_resp = urllib2.urlopen(request)
        return url_resp.read()

    def upload_forever_video(self, access_token, file_path, media_type, title="",introduction=""):
        # 视频文件
        open_file = open(file_path, "rb")
        param = {'media': open_file,'description':{"title":title,"introduction":introduction}}
        post_data, post_headers = poster.encode.multipart_encode(param)
        post_url = "https://api.weixin.qq.com/cgi-bin/material/add_material?access_token=%s&type=%s" %(access_token, media_type)
        request = urllib2.Request(post_url, post_data, post_headers)
        url_resp = urllib2.urlopen(request)
        return url_resp.read()