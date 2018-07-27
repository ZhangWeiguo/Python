# -*- coding: utf-8 -*-
# created by zwg in 20180617
import web,os,sys
sys.path.append("..")
from init import logger
from utils import get_template_path
from db import check_user

class User:
    def GET(self):
        logger.info("")
        path = get_template_path("user.html")
        render = web.template.frender(path)
        return render()