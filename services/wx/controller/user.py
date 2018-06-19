# -*- coding: utf-8 -*-
# created by zwg in 20180617
import sys
sys.path.append("..")
from init import ini_configer,logger
import web
import requests,json

class User:
    def GET(self):
        web_input = web.input()
        try:
            code = web_input.code
            state = web_input.state
        except:
            code = "error"
            state = "error"
        app_id = ini_configer.get("app-test","app_id")
        app_secret = ini_configer.get("app-test","app_secret")
        url = "https://api.weixin.qq.com/sns/oauth2/access_token?" + \
        "appid=%s&secret=%s&code=%s&grant_type=authorization_code"%(app_id,app_secret,code)
        res = requests.request("Get",url).text
        res_json = json.loads(res)
        try:
            access_token = res_json["access_token"]
            openid = res_json["openid"]
            user_url = "https://api.weixin.qq.com/sns/userinfo?access_token=%s&openid=%s&lang=zh_CN"%(access_token,openid)
            user_res = requests.request("Get",user_url).text
        except:
            user_res = "error"
        return "Get User data:" + web.data() + "\n   res: " + res + "\n   user_res: " + user_res 
    def POST(self):
        web_input = web.input()
        try:
            code = web_input.code
            state = web_input.state
        except:
            code = "error"
            state = "error"
        app_id = ini_configer.get("app-test","app_id")
        app_secret = ini_configer.get("app-test","app_secret")
        url = "https://api.weixin.qq.com/sns/oauth2/access_token?" + \
        "appid=%s&secret=%s&code=%s&grant_type=authorization_code"%(app_id,app_secret,code)
        res = requests.request("Get",url).text
        res_json = json.loads(res)
        try:
            access_token = res_json["access_token"]
            openid = res_json["openid"]
            user_url = "https://api.weixin.qq.com/sns/userinfo?access_token=%s&openid=%s&lang=zh_CN"%(access_token,openid)
            user_res = requests.request("Get",user_url).text
        except:
            user_res = "error"
        return "Get User data:" + web.data() + "\n   res: " + res + "\n   user_res: " + user_res 