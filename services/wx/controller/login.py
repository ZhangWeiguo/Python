# -*- coding: utf-8 -*-
# created by zwg in 20180617
import sys
sys.path.append("..")
from init import ini_configer,logger
import web

class Login:
    def GET(self):
        login = web.template.frender('static/login.html')
        return login()
    def POST(self):
        web_input = web.input()
        web_data = web.data()
        logger.info("Post Data: %s"%web_data)
        for item in web_input.items():
            logger.info(item[0] + item[1].encode("utf-8"))
        return "Post Data: %s"%web_data