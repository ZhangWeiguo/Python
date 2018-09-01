# -*- coding: utf-8 -*-
# created by zwg in 20180727
import web,os,sys
sys.path.append("..")
from init import logger
from utils import get_template_path
from db import check_user,get_default_blog,get_blog

class Blog:
    def GET(self):
        logger.info("%s Get The Blog Page"%web.cookies().get("session_id"))
        data = web.input()
        try:
            blog_id = int(data.blog_id)
        except:
            result,blog_id = get_default_blog()
        result,blog_data = get_blog(blog_id)
        path = get_template_path("blog.html")
        render = web.template.frender(path)
        return render(blog_data)