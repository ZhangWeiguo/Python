# -*- coding: utf-8 -*-
# created by zwg in 20180727
import web,os,sys
sys.path.append("..")
from init import logger,global_data
from utils import get_template_path


class Cate:
    def GET(self, cate):
        logger.info("%s Get The Cate Page"%web.cookies().get("session_id"))
        try:
            user_name = web.config.session["user_name"]
            user_page = "/user/%s"%(user_name)
        except:
            user_name = "登录"
            user_page = "/login"
        if user_name == "":
            user_name = "登录"
            user_page = "/login"
        user_data = {"user_name":user_name,"user_page":user_page}
        cate_data = []
        path = get_template_path("cate.html")
        render = web.template.frender(path)
        blog_cate = global_data["html_data"]["blog_cate"].keys()
        for one in blog_cate:
            cate_data.append({"name":one,"url":"/cate/%s"%one})
        return render(user_data, cate_data)

