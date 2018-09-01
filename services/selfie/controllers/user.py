# -*- coding: utf-8 -*-
# created by zwg in 20180617
import web,os,sys
sys.path.append("..")
from init import logger,global_data
from utils import get_template_path
from db import check_user,get_user_data

class User:
    def GET(self, user_name):
        logger.info("%s Get The User Page"%web.cookies().get("session_id"))

        try:
            user_name = web.config.session["user_name"]
            user_page = "/user/%s"%(user_name)
        except:
            user_name = "登录"
            user_page = "/login"
        if user_name == "":
            user_name = "登录"
            user_page = "/login"
        if user_name != "登录":
            result,user_info,user_blog = get_user_data(user_name)
        
        if result:
            user_data["user_info"] = user_info
            user_data["user_blog"] = user_blog
        user_data["user_name"] = user_name
        user_data["user_page"] = user_page

        cate_data = []
        blog_cate = global_data["html_data"]["blog_cate"].keys()
        for one in blog_cate:
            cate_data.append({"name":one,"url":"/cate/%s"%one})
        

        path = get_template_path("user.html")
        render = web.template.frender(path)
        return render(user_data, cate_data)