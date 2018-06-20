# -*- coding: utf-8 -*-
# created by zwg in 20180617
import sys
sys.path.append("..")
from init import ini_configer,logger,auth
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
        res = auth.get_detail_userinfo(code, state)
        return "Get User data:" + web.data() + "\n   res: " + res
    def POST(self):
        web_input = web.input()
        try:
            code = web_input.code
            state = web_input.state
        except:
            code = "error"
            state = "error"
        res = auth.get_detail_userinfo(code, state)
        return "Get User data:" + web.data() + "\n   res: " + res