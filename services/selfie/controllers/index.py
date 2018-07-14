# -*- coding: utf-8 -*-
# created by zwg in 20180617
import web,os


class Index:
    def GET(self):
        try:
            user_name = web.config.session["user_name"]
            user_page = "/%s"%(user_name)
        except:
            user_name = "登录"
            user_page = "/login"
        data = {"user_name":user_name,"user_page":user_page}
        s = os.path.join('templates','index.html')
        render = web.template.frender(s)
        return render(data)
    def POST(self):
        try:
            user_name = web.config.session["user_name"]
            user_page = "/%s"%(user_name)
        except:
            user_name = "登录"
            user_page = "/login"
        data = {"user_name":user_name,"user_page":user_page}
        s = os.path.join('templates','index.html')
        render = web.template.frender(s)
        return render(data)