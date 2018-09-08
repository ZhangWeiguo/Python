# -*- coding: utf-8 -*-
# created by zwg in 20180908
import web,json
from init import logger,global_data

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
        try:
            data = data.data
        except:
            data = {}
        if source == "cate_detail":
            result["succ"] = True
            result["data"] = global_data["html_data"]["blog_cate"]
        return json.dumps(result)
        
