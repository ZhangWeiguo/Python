# -*- coding: utf-8 -*-
# created by zwg in 20180617
import time

class Msg(object):
    def __init__(self):
        pass
    def send(self):
        return "success"

class TextMsg(Msg):
    def __init__(self, to_username, from_username, content):
        self.__dict = dict()
        self.__dict['ToUserName'] = to_username
        self.__dict['FromUserName'] = from_username
        self.__dict['CreateTime'] = int(time.time())
        self.__dict['Content'] = content
    def send(self):
        xml_form = """
        <xml>
        <ToUserName><![CDATA[{ToUserName}]]></ToUserName>
        <FromUserName><![CDATA[{FromUserName}]]></FromUserName>
        <CreateTime>{CreateTime}</CreateTime>
        <MsgType><![CDATA[text]]></MsgType>
        <Content><![CDATA[{Content}]]></Content>
        </xml>
        """
        return xml_form.format(**self.__dict)

class ImageMsg(Msg):
    def __init__(self, to_username, from_username, media_id):
        self.__dict = dict()
        self.__dict['ToUserName'] = to_username
        self.__dict['FromUserName'] = from_username
        self.__dict['CreateTime'] = int(time.time())
        self.__dict['MediaId'] = media_id
    def send(self):
        xml_form = """
        <xml>
        <ToUserName><![CDATA[{ToUserName}]]></ToUserName>
        <FromUserName><![CDATA[{FromUserName}]]></FromUserName>
        <CreateTime>{CreateTime}</CreateTime>
        <MsgType><![CDATA[image]]></MsgType>
        <Image>
        <MediaId><![CDATA[{MediaId}]]></MediaId>
        </Image>
        </xml>
        """
        return xml_form.format(**self.__dict)