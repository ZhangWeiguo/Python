# -*-encoding:utf8-*-

import urllib2, urllib, hashlib, time, json



class WaApi():
    def __init__(self):
        self.table_url = 'http://api.in.wa.uc.local:32006/api/queryStatKeyCode'
        self.log_url = 'http://tunnel.in.wa.uc.local:22310/tunnel/get_log'
        self.keyCode = "a9603ba96edd426eb47596f158eb579e"
        self.secretKey = "87986d6717c34c16b34c58289feeea73"
        self.app = "30001"
    def GetTable(self,statKey,statId,begin,end,dataFilters):
        P = {}
        P['app'] = self.app
        P['statKey'] = statKey
        P['statId'] = statId
        P['from'] = begin
        P['to'] = end
        P['tm'] = long(time.time()) * 1000
        s = P['app'] + P['statKey'] + P['from'] + P['to'] + str(P['tm']) + self.secretKey + self.keyCode
        P['sign'] = sign = hashlib.md5(s).hexdigest()
        P['needOriginDimValue'] = "false"
        P['keyCode'] = self.keyCode
        P["dataFilters"] = dataFilters
        request = urllib2.Request(url=self.table_url, data=urllib.urlencode(P))
        page = urllib2.urlopen(request)
        result = page.read()
        R = json.loads(result)
        return R


def get_video_score(video_id,date,country):
    statKey = "16727"
    statId = "16727_dim_1"
    begin = "%s 00:00"%date
    end = "%s 00:00"%date
    dataFilters = '[{"field": "video_id", "operator": "str_eq_ignorecase", "value": "%s"},\
                        {"field": "country", "operator": "str_eq_ignorecase", "value": "%s"}]'%(video_id,country)
    Wa = WaApi()
    R = Wa.GetTable(statKey, statId, begin, end, dataFilters)

    result = {"score":0,"status":"normal"}
    if not R['success']:
        result['status'] = "error"
    else:
        data = R['data']['data']
        if len(data) == 0:
            result['status'] = "error"
        else:
            data0 = data[0]
            result['score'] = data0['score']
    return result


if __name__ == "__main__":
    R = get_video_score("awftlnep5uw","2017-11-21","IN")
    print R

