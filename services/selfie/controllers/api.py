# -*- coding: utf-8 -*-
# created by zwg in 20180908
import web,json,time
from init import logger,global_data
from db import get_blog,add_blog
'''
Input
    GET
        source=cate_detail
        source=blog_info&blog_id=$blog_id
    POST
        source=add_blog&......
    

Output  {succ:True,data:{}}
'''
class API:
    def GET(self):
        data = web.input()
        result = {"succ":False,"data":{}}
        try:
            source = data.source
        except:
            source = ""
        if source == "cate_detail":
            result["succ"] = True
            result["data"] = global_data["html_data"]["blog_cate"]
        elif source == "blog_info":
            try:
                blog_id = int(data.blog_id)
                query_result = get_blog(blog_id)
                if query_result["succ"] == True:
                    result["succ"] = True
                    result["data"] = query_result["data"]
            except:
                pass
        else:
            pass
        return json.dumps(result)
    def POST(self):
        result = {"succ":False,"data":{}}
        try:
            user_name = web.config.session["user_name"]
        except:
            user_name = ""
        if user_name != "":
            data = web.input()
            try:
                source = data.source
            except:
                source = ""
            if source == "add_blog":
                blog_title = data.title
                blog_abstract = data.abstract
                blog_content = data.content
                blog_creator = user_name
                blog_cate = data.cate
                blog_sub_cate = data.sub_cate
                exec_result = add_blog(blog_creator,blog_title,blog_abstract,blog_content,blog_cate,blog_sub_cate)
                if exec_result == True:
                    result["succ"] = True
        return json.dumps(result)
        
