# -*- coding: utf-8 -*-
# created by zwg in 20180727
import web,os,sys
sys.path.append("..")
from init import logger
from utils import get_template_path
from db import check_user,get_cate_blog

class Catalog:
    def GET(self, cate):
        logger.info("%s Get The Catalog Page"%web.cookies().get("session_id"))
        data = web.input()
        try:
            page_num = data.page_num
            blog_id = data.blog_id
        except:
            page_num = 1
            blog_id = 0
        page_size = 20
        result,blog_cate,all_page_num = get_cate_blog(page_size, page_num, cate)
        if result:
            if blog_id == 0:
                blog_id = min([one["blog_id"] for one in blog_cate])
            path = get_template_path("catalog.html")
            render = web.template.frender(path)
            return render(blog_cate)
        else:
            web.seeother("/unknow")

