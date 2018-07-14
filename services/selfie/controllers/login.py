# -*- coding: utf-8 -*-
# created by zwg in 20180617
import web,os,sys
sys.path.append("..")
from init import logger
from db import check_user

class Login:
    def GET(self):
        render = web.template.frender("templates/login.html")
        return render()

    def POST(self):
        logger.info(web.data())
        data = web.input()
        try:
            user_name = data.user_name
            pass_word = data.pass_word
        except:
            user_name = ""
            pass_word = ""
        if user_name != "" and pass_word != "":
            web.config.session["user_name"] = user_name
            web.config.session["pass_word"] = pass_word
            result, info = check_user(user_name, pass_word)
            if result:
                web.seeother("/index")
        render = web.template.frender("templates/login.html")
        return render()
