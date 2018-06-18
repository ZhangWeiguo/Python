# -*- coding: utf-8 -*-
# created by zwg in 20180617
import web

class Login:
    def GET(self):
        login = web.template.frender('static/login.html')
        return login()
    def POST(self):
        return "Post OK"