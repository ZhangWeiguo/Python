# -*- coding: utf-8 -*-
# created by zwg in 20180727
import web,os,sys
sys.path.append("..")
from init import logger,global_data
from utils import get_template_path
from db import get_cate_blog,add_blog_pv,get_blog_cate


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
        blog_cate = global_data["html_data"]["blog_cate"].keys()
        for one in blog_cate:
            cate_data.append({"name":one,"url":"/cate/%s"%one})

        data = web.input()
        try:
            page_num = int(data.page_num)
            blog_id = int(data.blog_id)
        except:
            page_num = 1
            blog_id = -1
        page_size = 20
        add_blog_pv(blog_id)
        result,cate_blog,all_page_num = get_cate_blog(page_size, page_num, cate)

        # 防止page_num乱输入
        if page_num <= 0 or page_num >= all_page_num:
            if page_num <= 0:
                page_num = 1
            if page_num >= all_page_num:
                page_num = all_page_num
            result,cate_blog,all_page_num = get_cate_blog(page_size, page_num, cate)

        # blog_id=-1 返回默认的blog，没有默认的则继续返回-1
        # blog_id 必须是属于该cate的类型，否则也返回默认的
        result,blog_id_cate = get_blog_cate(blog_id)
        if blog_id == -1 or blog_id_cate != cate:
            try:
                blog_id = min([one["blog_id"] for one in cate_blog])
            except:
                pass

        catalog_data = {}
        catalog_data["blog_id"] = blog_id
        catalog_data["all_page_num"] = all_page_num
        catalog_data["page_num"] = page_num
        catalog_data["cate_blog"] = cate_blog

        path = get_template_path("cate.html")
        render = web.template.frender(path)
        


        return render(user_data, cate_data, catalog_data)

