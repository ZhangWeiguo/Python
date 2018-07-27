# -*- coding: utf-8 -*-
# created by zwg in 20180727
import web,os,sys
sys.path.append("..")
from init import logger
from utils import get_template_path
from db import check_user

class Blog:
    def GET(self):
        path = get_template_path("blog.html")
        render = web.template.frender(path)
        return render()