# -*- coding: utf-8 -*-
# created by zwg in 20180617
import sys
sys.path.append("../../basic")
from logger import Logger
from config_parse import IniConfiger
from config_parse import XmlConfiger


ini_configer = IniConfiger("config.ini")
app_name = ini_configer.get("app","app_name")
log_path = ini_configer.get("log","log_path")
keep_num = ini_configer.get("log","keep_num")
logger = Logger(app_name=app_name,file_name=log_path,keep_num=keep_num)



