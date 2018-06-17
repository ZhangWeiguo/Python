# -*- coding: utf-8 -*-
# filename: menu.py
import urllib
from token_access import TokenAccess

class Menu(object):
    def __init__(self):
        pass
    def create(self, post_data, access_token):
        post_url = "https://api.weixin.qq.com/cgi-bin/menu/create?access_token=%s" % access_token
        if isinstance(post_data, unicode):
            post_data = post_data.encode('utf-8')
        url_resp = urllib.urlopen(url=post_url, data=post_data)
        print url_resp.read()

    def query(self, access_token):
        post_url = "https://api.weixin.qq.com/cgi-bin/menu/get?access_token=%s" % access_token
        url_resp = urllib.urlopen(url=post_url)
        print url_resp.read()

    def delete(self, access_token):
        post_url = "https://api.weixin.qq.com/cgi-bin/menu/delete?access_token=%s" % access_token
        url_resp = urllib.urlopen(url=post_url)
        print url_resp.read()

    #获取自定义菜单配置接口
    def get_current_selfmenu_info(self, access_token):
        post_url = "https://api.weixin.qq.com/cgi-bin/get_current_selfmenu_info?access_token=%s" % access_token
        url_resp = urllib.urlopen(url=post_url)
        print url_resp.read()