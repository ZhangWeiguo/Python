# -*- coding: utf-8 -*-
# created by zwg in 20180917
import web,os,sys
sys.path.append("..")
from utils import get_template_path


class EditBlog:
    def GET(self):
        logger.info("%s Get The EditBlog Page"%web.cookies().get("session_id"))
        path = get_template_path("edit_blog.html")
        render = web.template.frender(path)
        return render()
