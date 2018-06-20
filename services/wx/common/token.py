# -*- coding: utf-8 -*-
# created by zwg in 20180620
# 响应微信token验证
import urllib
import time
import json
class Token:    
    def __init__(self, app_id, app_secret):        
        self.__access_token  =   '' 
        self.__left_time     =   0
        self.app_id         =   app_id
        self.app_secret     =   app_secret
    def __real_get_access_token(self):  
        app_id = self.app_id
        app_secret = self.app_secret    
        post_url = "https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s" \
                            % (app_id, app_secret)      
        url_resp = urllib.urlopen(post_url)
        url_resp = json.loads(url_resp.read())
        self.__access_token = url_resp['access_token']
        self.__left_time = url_resp['expires_in']
    def get_access_token(self):
        if self.__left_time < 10:
            self.__real_get_access_token()
            return self.__access_token
    def run(self):
        while(True):
            if self.__left_time > 10:
                time.sleep(2)
                self.__left_time -= 2
            else:
                self.__real_get_access_token()

                