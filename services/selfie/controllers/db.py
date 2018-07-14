# -*- coding: utf-8 -*-
# created by zwg in 20180713
import sys
sys.path.append("..")
from init import logger,mysql_client



def check_user(user_name, pass_word):
    sql = "select * from user_info where user_name='%s' and pass_word='%s'"%(user_name, pass_word)
    result = mysql_client.query(sql)
    if result['succ'] == True:
        n = len(result['data'])
        if n == 1:
            return True,result['data'][0]
    return False,{}
