# -*- coding: utf-8 -*-
# created by zwg in 20180617
import web,os


class User:
    def GET(self,user_name):
        return "hello %s"%(user_name)
    def POST(self,user_name):
        return "hello %s"%(user_name)