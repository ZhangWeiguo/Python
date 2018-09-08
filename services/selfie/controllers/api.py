# -*- coding: utf-8 -*-
# created by zwg in 20180908
import web,json
from init import logger,global_data
from db import get_blog
'''
Input   source=$source&data=data
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
        return json.dumps(result)
        
