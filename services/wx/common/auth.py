# -*- coding: utf-8 -*-
# created by zwg in 20180620
# 获取用户授权
import requests

class Auth(object):
    def __init__(self, app_id, app_secret):
        self.app_id = app_id
        self.app_secret = app_secret
        self.session = requests.Session()
    def get_detail_userinfo(self, code, state):
        url = "https://api.weixin.qq.com/sns/oauth2/access_token?appid=%s&secret=%s&code=%s&grant_type=authorization_code"
        url = url%(self.app_id,self.app_secret,code)
        res = self.session.request("Get",url).text
        try:
            res_json = json.loads(res)
            access_token = res_json["access_token"]
            openid = res_json["openid"]
            user_url = "https://api.weixin.qq.com/sns/userinfo?access_token=%s&openid=%s&lang=zh_CN"%(access_token,openid)
            user_res = self.session.request("Get",user_url).text
        except:
            return res
        return user_res
    def get_base_userinfo(self):
        pass