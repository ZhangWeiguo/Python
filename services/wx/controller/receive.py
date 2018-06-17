# -*- coding: utf-8 -*-
# created by zwg in 20180617
import xml.etree.ElementTree as ET

class Msg(object):
    def __init__(self, xml_data):
        self.to_usermame    = xml_data.find('ToUserName').text
        self.from_username  = xml_data.find('FromUserName').text
        self.create_time    = xml_data.find('CreateTime').text
        self.msg_type       = xml_data.find('MsgType').text

class EventMsg(object):
    def __init__(self, xml_data):
        self.to_usermame    = xml_data.find('ToUserName').text
        self.from_username  = xml_data.find('FromUserName').text
        self.create_time    = xml_data.find('CreateTime').text
        self.msg_type       = xml_data.find('MsgType').text
        self.event          = xml_data.find('Event').text

class Click(EventMsg):
    def __init__(self, xml_data):
        EventMsg.__init__(self, xml_data)
        self.event_key = xml_data.find('EventKey').text

class ImageMsg(Msg):
    def __init__(self, xml_data):
        Msg.__init__(self, xml_data)
        self.pic_url = xml_data.find('PicUrl').text
        self.media_id = xml_data.find('MediaId').text

class TextMsg(Msg):
    def __init__(self, xml_data):
        Msg.__init__(self, xml_data)
        self.content = xml_data.find('Content').text.encode("utf-8")

class UnknowMsg(Msg):
    def __init__(self, xml_data):
        Msg.__init__(self, xml_data)
        self.content ="Unknow Message"

def parse_xml(web_data):
    if len(web_data) == 0:
        return None
    xml_data = ET.fromstring(web_data)
    msg_type = xml_data.find('MsgType').text
    if msg_type == 'event':
        event_type = xml_data.find('Event').text
        if event_type == 'CLICK':
            return Click(xml_data)
    elif msg_type == 'text':
        return TextMsg(xml_data)
    elif msg_type == 'image':
        return ImageMsg(xml_data)
    else:
        return UnknowMsg(xml_data)

