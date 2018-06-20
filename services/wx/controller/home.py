# -*- coding: utf-8 -*-
# created by zwg in 20180617
import web
class Home:
    def GET(self):
        login = web.template.frender('static/index.html')
        return login()
    def POST(self):
        login = web.template.frender('static/index.html')
        return login()