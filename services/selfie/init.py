# -*- coding: utf-8 -*-
# created by zwg in 20180713
import sys
sys.path.append("../../basic")
from logger import Logger
from mysql_client import MysqlClient
from config_parse import IniConfiger

ini_configer 	            = IniConfiger("main.ini")
app_name    	            = ini_configer.get("log","app_name")
file_name    	            = ini_configer.get("log","file_name")
keep_num    	            = ini_configer.get("log","keep_num")
when    	                = ini_configer.get("log","when")
rotate    	                = ini_configer.get("log","rotate")
logger      	            = Logger(
                                app_name    = app_name,
                                file_name   = file_name,
                                keep_num    = keep_num,
                                when        = when,
                                rotate      = rotate)

mysql_config                = {}
mysql_config["user"]        = ini_configer.get("mysql","username")
mysql_config["password"]    = ini_configer.get("mysql","password")
mysql_config["host"]        = ini_configer.get("mysql","host")
mysql_config["port"]        = int(ini_configer.get("mysql","port"))
mysql_config["database"]    = ini_configer.get("mysql","database")

mysql_client                = MysqlClient(mysql_config)

