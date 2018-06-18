# -*- coding: utf-8 -*-
# created by zwg in 20180617
import sys
sys.path.append("..")
from init import ini_configer,logger
import reply
import receive
import web,hashlib

class Wx(object):
    # 处理信息交互
    def POST(self):
        web_data = web.data()
        info = "Post Data: %s"%(str(web_data).replace("\n",""))
        logger.info(info)
        rec_msg = receive.parse_xml(web_data)
        if isinstance(rec_msg, receive.Msg):
            to_user = rec_msg.from_username
            from_user = rec_msg.to_usermame
            if isinstance(rec_msg, receive.TextMsg):
                question = rec_msg.content
                answer   = u"对不起，这个问题我不知道\n".encode('utf-8') + question
                reply_msg = reply.TextMsg(to_user, from_user, answer)
                return reply_msg.send()
            elif isinstance(rec_msg, receive.ImageMsg):
                media_id = rec_msg.media_id
                reply_msg = reply.ImageMsg(to_user, from_user, media_id)
                return reply_msg.send()
            else:
                content = u"编写中，尚未完成".encode('utf-8')
                reply_msg = reply.TextMsg(to_user, from_user, content)
                return reply_msg.send()
        elif isinstance(rec_msg,receive.EventMsg):
            to_user = rec_msg.from_username
            from_user = rec_msg.to_usermame
            reply_msg = reply.TextMsg(to_user, from_user, u"这是个事件，具体做什么我还没想好".encode("utf-8"))
            return reply_msg.send()
        else:
            to_user = rec_msg.from_username
            from_user = rec_msg.to_usermame
            reply_msg = reply.TextMsg(to_user, from_user, u"这是个我未定义的类型".encode("utf-8"))
            return reply_msg.send()
        
    # 初始化认证
    def GET(self):
        try:
            data = web.input()
            if len(data) == 0:
                return ""
            logger.info("Get Data:"+str(data.items()))
            signature   = data.signature
            timestamp   = data.timestamp
            nonce       = data.nonce
            echostr     = data.echostr
            token       = ini_configer.get("app","token")
            L = [token, timestamp, nonce]
            L.sort()
            sha1 = hashlib.sha1()
            map(sha1.update, L)
            hashcode = sha1.hexdigest()
            logger.info("Token Access:"+"handle/GET func: hashcode, signature: "+ hashcode+ signature)
            if hashcode == signature:
                logger.info("Token Succ")
                return echostr
            else:
                logger.info("Token Error")
                return ""
        except Exception, Argument:
            logger.info("Token Fail")
            return Argument