# -*- coding: utf-8 -*-
# created by zwg in 20180617
import web,os,sys
sys.path.append("..")
from init import logger,global_data
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
        logger.info("POST: %s Login The Index Page"%user_name)
        cate = []
        blog_cate = global_data["html_data"]["blog_cate"].keys()
        for one in blog_cate:
            cate.append({"name":one,"url":"#"})
        return render(data, cate)
    def POST(self):
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
        logger.info("GET: %s Login The Index Page"%user_name)
        cate = []
        blog_cate = global_data["blog_cate"].keys()
        for one in blog_cate:
            cate.append({"name":one,"url":"#"})
        return render(data, cate)