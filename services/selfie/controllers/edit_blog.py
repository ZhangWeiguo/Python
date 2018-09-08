# -*- coding: utf-8 -*-
# created by zwg in 20180917
import web,os,sys
sys.path.append("..")
from utils import get_template_path
from init import logger,global_data
from db import get_blog

class EditBlog:
    def GET(self):
        logger.info("%s Get The Index Page"%web.cookies().get("session_id"))
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
        path = get_template_path("index.html")
        render = web.template.frender(path)
        logger.info("GET: %s Login The Index Page"%user_name)
        cate_data = []
        blog_cate = global_data["html_data"]["blog_cate"].keys()
        for one in blog_cate:
            cate_data.append({"name":one,"url":"/cate/%s"%one})

        path = get_template_path("edit_blog.html")
        render = web.template.frender(path)

        data = web.input()
        try:
            blog_id = int(data.blog_id)
            query_result = get_blog(blog_id)
            if query_result["succ"] == True:
                blog_info = query_result["data"]
        except:
            blog_info = {}
        return render(user_data, cate_data, blog_info)
