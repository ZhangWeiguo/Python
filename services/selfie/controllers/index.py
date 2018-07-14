# -*- coding: utf-8 -*-
# created by zwg in 20180617
import web,os


class Index:
    def GET(self):
        s = os.path.join('templates','index.html')
        render = web.template.frender(s)
        return render()
    def POST(self):
        s = os.path.join('templates','index.html')
        render = web.template.frender(s)
        return render()