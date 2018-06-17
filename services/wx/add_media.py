# -*- coding: utf-8 -*-
# created by zwg in 20180617
from common.token_access import TokenAccess
from common.media import Media
import json
from init import ini_configer

if __name__ == '__main__':
    my_media = Media()
    token_access = TokenAccess(app_id=ini_configer.get("app-test","app_id"),app_secret=ini_configer.get("app-test","app_secret"))
    access_token = token_access.get_access_token()
    file_path = "static/test.jpg"
    media_type = "image"
    res = my_media.uplaod(access_token, file_path, media_type)
    print res
    res = json.loads(res)
    media_id = res["media_id"]
    my_media.download(access_token=access_token, media_id=media_id, media_path="1.jpg")
    res = my_media.upload_forever_media(access_token, file_path, media_type)
    print res