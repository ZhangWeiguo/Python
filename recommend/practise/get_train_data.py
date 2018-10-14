# -*-encoding:utf-8-*-

import urllib2,urllib,md5,time,json
from conf import action as all_action
def write2txt(messages, filename):
    f = file(filename,'a+')
    f.writelines(messages)
    f.close()

def get_log(month,day,hour,filename):
    base_url = 'http://XXXX/get_log'
    P = {}
    P["app"] = "30001"
    P["type"] = "pre_rawlog"
    P["code"] = "action-log-in-v1"
    P["from"] = "2017%s%s%s"%(str(month).zfill(2),str(day).zfill(2),str(hour).zfill(2))
    P["to"] = "2017%s%s%s"%(str(month).zfill(2),str(day).zfill(2),str(hour).zfill(2))
    P["tm"] = long( time.time() ) * 1000
    P["keyCode"] = "XXX"
    secretKey = "XXX"
    M = md5.new()
    M.update(P.get("app") + P.get("code") + str(P.get("tm")) + P.get("from") + P.get("to") + secretKey + P.get("keyCode"))
    P['sign'] = M.hexdigest()
    url = base_url + "?" + urllib.urlencode(P)
    result = urllib2.urlopen(url).read()
    R = json.loads(result)
    S = json.loads(urllib2.urlopen(R['check_link']).read())
    links_dict = S['links']
    for link_dict in links_dict:
        link = link_dict['link']
        all_data = urllib2.urlopen(link).read()
        data = all_data.split('\n')
        messages = []
        for one in data:
            try:
                utdid,video_ids,action=parse_log(one)
                if action in all_action:
                    for video_id in video_ids:
                        messages.append("%s,%s,%s\n"%(utdid,video_id,action))
            except:
                pass
        write2txt(messages,filename)
        print "write %d messages"%(len(messages))




def parse_log(log_message):
    utdid = ""
    video_ids = []
    action = ""
    action_code = ""
    way = ""
    video_duration = 0
    watch_duration = 0
    logs = log_message.split('`')
    for i in logs:
        if "utdid=" in i:
            utdid = i[6:]
        if "action_code=" in i:
            action_code = i[12:]
        if "log_content=" in i:
            J = json.loads(i[12:])
            if "video_id" in J:
                video_ids.append(J["video_id"])
            elif "video_ids" in J:
                video_idss = J["video_ids"]
                video_ids = video_idss.split(",")
            if "action" in J:
                action = J["action"]
            if "way" in J:
                way = J["way"]
            if "video_duration" in J:
                video_duration = float(J["video_duration"])
            if "watch_duration" in J:
                watch_duration = float(J["watch_duration"])
    if action_code == "ugc_video_show":
        action = "show"
    elif action == "video_play_start" and way == "click":
        action = "play_click"
    elif action == "video_play_start" and way != "click":
        action = "play_slide"
    elif action == "video_play_exit":
        complete = watch_duration/video_duration
        if complete<0:
            complete = complete/(-1500.0)
        if complete >= 0.9:
            action = "play_complete"
        elif complete <0.9 and complete>=0.7:
            action = "play_uncomplete_8"
        elif complete <0.7 and complete>=0.4:
            action = "play_uncomplete_5"
        elif complete<0.4 and complete>=0.1:
            action = "play_uncomplete_2"
        else:
            action = "play_uncomplete_0"
    elif action == "video_like":
        action = "like"
    elif action_code == "ugc_follow":
        action = "follow"
    elif action_code == "ugc_video_share":
        action = "share"
    elif action_code == "ugc_video_comment":
        action = "comment"
    else:
        action = "unknow"
    return utdid,video_ids,action



    
if __name__ == "__main__":
    for i in range(24):
        try:
            get_log(12, 1, i, "data\\action1201%s.log" % str(i).zfill(2))
        except:
            pass
