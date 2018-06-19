# -*- coding: utf-8 -*-
# created by zwg in 20180617
from common.token_access import TokenAccess
from common.menu import Menu
import json
from urllib import quote
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
                        "name": "直接登录",
                        "url": "http://111.230.222.74/login"
                    },
                    {
                        "type": "view",
                        "name": "授权登录",
                        "url": "%s"
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
    # print my_menu.delete(access_token)
    app_id=ini_configer.get("app-test","app_id")
    url = "http://111.230.222.74/user"
    auth_url = "https://open.weixin.qq.com/connect/oauth2/authorize?appid=%s" + \
                "&redirect_uri=%s&response_type=code&scope=snsapi_userinfo" + \
                "&state=zhangweiguo#wechat_redirect"
    auth_url = auth_url%(app_id, quote(url))
    print auth_url
    button_json = post_json%(auth_url)
    # print my_menu.create(button_json, access_token)