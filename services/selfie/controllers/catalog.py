# -*- coding: utf-8 -*-
# created by zwg in 20180727
import web,os,sys
sys.path.append("..")
from init import logger
from utils import get_template_path
from db import check_user

class Catalog:
    def GET(self, cate):
        path = get_template_path("catalog.html")
        render = web.template.frender(path)
        return render()