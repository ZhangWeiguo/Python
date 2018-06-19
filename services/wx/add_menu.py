# -*- coding: utf-8 -*-
# created by zwg in 20180617
from common.token_access import TokenAccess
from common.menu import Menu
import json
from init import ini_configer

if __name__ == '__main__':
    my_menu = Menu()
    button_setting = '''{
        "button":
        [
            {
                "type": "click",
                "name": "热门消息",
                "key":  "mpGuide"
            },
            {
                "name": "公众平台",
                "sub_button":
                [
                    {
                        "type": "view",
                        "name": "更新公告",
                        "url": "http://111.230.222.74/login"
                    },
                    {
                        "type": "view",
                        "name": "接口权限说明",
                        "url": "http://mp.weixin.qq.com/wiki?t=resource/res_main&id=mp1418702138&token=&lang=zh_CN"
                    },
                    {
                        "type": "view",
                        "name": "返回码说明",
                        "url": "http://mp.weixin.qq.com/wiki?t=resource/res_main&id=mp1433747234&token=&lang=zh_CN"
                    }
                ]
            },
            {
                "type": "media_id",
                "name": "旅行",
                "media_id": "g9H60htjMlG0C6la55kXwvhuOSlfAj1V8QabYqdQfB0"
            }
          ]
    }'''

    post_json = button_setting
    token_access = TokenAccess(
                                app_id=ini_configer.get("app-test","app_id"),
                                app_secret=ini_configer.get("app-test","app_secret"))
    access_token = token_access.get_access_token()
    my_menu.delete(access_token)
    my_menu.create(post_json, access_token)