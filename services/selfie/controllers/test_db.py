# -*- encoding:utf-8 -*-
import sys
sys.path.append("../../../basic")
from mysql_client import MysqlClient

mysql_config                = {}
mysql_config["user"]        = "weog"
mysql_config["password"]    = 'wego1234'
mysql_config["host"]        = "127.0.0.1"
mysql_config["port"]        = 3306
mysql_config["database"]    = "selfie"
mysql_client                = MysqlClient(**mysql_config)


def check_user(user_name, pass_word):
    sql = "select * from user_info where user_name='%s' and pass_word='%s'"%(user_name, pass_word)
    result = mysql_client.query(sql)
    if result['succ'] == True:
        n = len(result['data'])
        if n == 1:
            return True,result['data'][0]
    else:
        msg = result['msg']
        logger.info("Mysql Check User Failed:" + msg )
    return False,{}

def get_user_info(user_name):
    sql = "select * from user_info where user_name='%s'"%(user_name)
    result = mysql_client.query(sql)
    if result['succ'] == True:
        n = len(result['data'])
        if n == 1:
            return True,result['data'][0]
    else:
        msg = result['msg']
        logger.info("Mysql Get User Info Failed:" + msg )
    return False,{}

def get_user_blog(user_name):
    sql = "select blog_id,user_name,title,abstract,create_time,cate,sub_cate,pv from blog_info where user_name='%s'"%(user_name)
    result = mysql_client.query(sql)
    if result['succ'] == True:
        n = len(result['data'])
        if n == 1:
            return True,result['data']
    else:
        msg = result['msg']
        logger.info("Mysql Get User Info Failed:" + msg )
    return False,[]


def get_user_data(user_name):
    user_info = {}
    user_blog = []
    result = False
    result,user_info = get_user_info(user_name)
    if result:
        user_info['create_time'] = time.strftime('yyyy-mm-dd HH:MM:SS', time.localtime(user_info['create_time']))
        result,user_blog = get_user_blog(user_name)
        if result:
            for blog in user_blog:
                blog["create_time"] = time.strftime('yyyy-mm-dd HH:MM:SS', time.localtime(blog['create_time']))
    return result,user_info,user_blog


user_data = get_user_data("NoTeethSmallPerson")
print user_data
