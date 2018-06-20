# -*- coding: utf-8 -*-
# created by zwg in 20180617
import sys
sys.path.append("../../basic")
from logger import Logger
from config_parse import IniConfiger
from config_parse import XmlConfiger
from common.auth import Auth
from common.token import Token


ini_configer = IniConfiger("config.ini")
app_id      =   ini_configer.get("app-test")
app_name    =   ini_configer.get("app-test","app_name")
app_token   =   ini_configer.get("app-test","token")
app_secret  =   ini_configer.get("app-test","app_secret")
log_path    =   ini_configer.get("log","log_path")
keep_num    =   ini_configer.get("log","keep_num")
logger      =   Logger(app_name=app_name,file_name=log_path,keep_num=keep_num,when='H',rotate = "Time")
auth        =   Auth(app_id=app_id,app_secret=app_secret)
token       =   Token(app_id=app_id,app_secret=app_secret)


