# -*- coding: utf-8 -*-
# created by zwg in 20180617
import web,os
from utils import get_template_path

class Index:
    def GET(self):
        try:
            user_name = web.config.session["user_name"]
            user_page = "/user/%s"%(user_name)
        except:
            user_name = "登录"
            user_page = "/login"
        if user_name == "":
            user_name = "登录"
            user_page = "/login"
        data = {"user_name":user_name,"user_page":user_page}
        path = get_template_path("index.html")
        render = web.template.frender(path)
        return render(data)
    def POST(self):
        try:
            user_name = web.config.session["user_name"]
            user_page = "/%s"%(user_name)
        except:
            user_name = "登录"
            user_page = "/login"
        data = {"user_name":user_name,"user_page":user_page}
        path = get_template_path("index.html")
        render = web.template.frender(path)
        return render(data)