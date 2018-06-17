import sys
sys.path.append("../../basic")

from config_parse import IniConfiger
configer = IniConfiger("wx_config.ini")
app_id = configer.get("token","app_id")
app_secret = configer.get("token","app_secret")
print app_id
# from basic import TokenAccess
# tokenAccess = TokenAccess(app_id=app_id,app_secret=app_secret)
# print tokenAccess.get_access_token()