# -*- coding: utf-8 -*-
# created by zwg in 20180721
import os,sys
sys.path.append("..")
from init import html_path


def get_template_path(name):
    path = os.path.join(html_path,name)
    return path