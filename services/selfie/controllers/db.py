# -*- coding: utf-8 -*-
# created by zwg in 20180713
import sys,time,math
sys.path.append("..")
from init import logger,mysql_client



def check_user(user_name, pass_word):
    sql = "select * from user_info where user_name='%s' and pass_word='%s'"%(user_name, pass_word)
    result = mysql_client.query(sql)
    print result
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

def get_user_blog(user_name, content = False):
    if content:
        sql = "select * from blog_info where user_name='%s' order by create_time desc"%(user_name)
    else:
        sql = "select blog_id,user_name,title,abstract,create_time,cate,sub_cate,pv \
        from blog_info where user_name='%s' order by create_time desc"%(user_name)
    result = mysql_client.query(sql)
    if result['succ'] == True:
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
        user_info['create_time'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(user_info['create_time']))
        result,user_blog = get_user_blog(user_name)
        if result:
            for blog in user_blog:
                blog["create_time"] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(blog['create_time']))
    return result,user_info,user_blog


###################################################################

def add_blog(user_name,title,abstract,content,cate,sub_cate):
    create_time = int(time.time())
    sql = '''insert into blog_info(
            user_name,title,abstract,content,cate,sub_cate,create_time
            ) values
            (
            %s,%s,%s,%s,%s,%s
            ) '''%(user_name,title,abstract,content,cate,sub_cate,create_time)
    result = mysql_client.execute(sql)
    if result['succ'] == True:
        return True
    else:
        msg = result['msg']
        logger.info("Mysql Add Blog Failed:" + msg )
    return False

def get_default_blog():
    sql = "select blog_id from blog_info order by pv desc limit 1"
    result = mysql_client.query(sql)
    if result["succ"] == True:
        if len(result["data"]) == 1:
            add_blog_pv(result["data"][0]["blog_id"])
            return True,result["data"][0]["blog_id"]
    msg = result["msg"]
    logger.info("Mysql Get Blog Failed:" + msg )
    return False,-1

def get_blog(blog_id):
    sql = "select * from blog_info where blog_id=%d"%(blog_id)
    result = mysql_client.query(sql)
    if result["succ"] == True:
        if len(result["data"]) == 1:
            add_blog_pv(blog_id)
            result["data"][0]["create_time"] = time.strftime('%Y-%m-%d %H:%M:%S', 
                            time.localtime(result["data"][0]["create_time"]))
            result["data"][0]["content"] = result["data"][0]["content"]
            return True,result["data"][0]
    msg = result["msg"]
    logger.info("Mysql Get Blog Failed:" + msg )
    return False,{}

def add_blog_pv(blog_id):
    sql = "update blog_info set pv=pv+1 where blog_id = '%s'"%blog_id
    result = mysql_client.execute(sql)
    if result['succ'] == True:
        return True
    else:
        msg = result['msg']
        logger.info("Mysql Add Blog PV Failed:" + msg )
    return False

###################################################################

# 返回 这一页的数据，且返回总页数
def get_cate_blog(page_size, page_num, cate):
    blog_cate = []
    all_page_num = 0
    final_result = False

    start = (page_num-1)*page_size + 1
    end = page_num*page_size
    sql = '''select 
            blog_id,user_name,title,abstract,create_time,sub_cate  
            from blog_info 
            where blog_id>=%d 
            and blog_id<=%d 
            and cate="%s"
            order by pv desc'''%(start, end, cate)
    sql_count = '''select count(1) as num 
            from blog_info 
            where cate="%s"'''%(cate)
    result = mysql_client.query(sql)
    if result["succ"] == True:
        blog_cate = result["data"]
        final_result = True
    else:
        blog_cate = []
        final_result = False
        msg = result["msg"]
        logger.info("Mysql Get Cate Failed:" + msg )

    result = mysql_client.query(sql_count)
    if result["succ"] == True:
        final_result = True
        all_page_num = result["data"][0]["num"]
    else:
        final_result = False
        msg = result["msg"]
        logger.info("Mysql Get Cate Num Failed:" + msg )

    all_page_num = math.ceil(all_page_num/page_size)
    
    return final_result,blog_cate,all_page_num

