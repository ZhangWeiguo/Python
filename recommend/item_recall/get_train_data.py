# -*- encoding:utf-8 -*-
# create by WegoZng 20180428
# 从WA下载每小时的训练数据

import time,urllib2,json,hashlib,urllib,os,re




def init_filename(file_name):
    f = file(file_name,'w')
    f.close()

def check_file(file_name):
    size = os.path.getsize(file_name)
    if size >= 10000:
        return True
    else:
        return False

def clear_file(file_path,keep_day):
    L = [os.path.join(file_path,i) for i in os.listdir(file_path)]
    fail_file = []
    t0 = time.time()
    keep_time = keep_day * 24 * 60 * 60
    for i in L:
        t = os.path.getctime(i)
        if t + keep_time > t0:
            pass
        else:
            try:
                os.rm(i)
            except:
                fail_file.append(i)
    return fail_file


def get_data(table_name, file_name, ymdh, local):
    t1 = time.time()
    e = ""
    try:
        waApi = WaApi(result = table_name, local = local)
        waApi.get_result(ymdh, file_name)
        t2 = time.time()
        result = True
    except Exception as e:
        result = False
    t2 = time.time()
    t = t2 - t1
    e = str(e)
    return result,t,e


class WaApi():
    def __init__(self,result="",local = False):
        # local ：是否本机，本机需要加IP白名单才能使用
        # table 使用table ID  string
        # result 使用原始日志名或tableId  string
        if local:
            self.log_url    = "https://tunnel-in-wa.uc.cn/tunnel/get_log"
            self.table_url  = "https://api-in-wa.uc.cn/api/queryStatKeyCode"
        else:
            self.log_url    = 'http://tunnel.in.wa.uc.local:22310/tunnel/get_log'
            self.table_url  = 'http://api.in.wa.uc.local:32006/api/queryStatKeyCode'

        self.keyCode                    = "a9603ba96edd426eb47596f158eb579e"
        self.secretKey                  = "87986d6717c34c16b34c58289feeea73"
        self.app                        = "30001"
        self.P1                         = {}
        self.P1['app']                  = self.app
        self.P1['statId']               = result + "_dim_1"
        self.P1['needOriginDimValue']   = "false"
        self.P1['keyCode']              = self.keyCode

        self.P2                         = {}
        self.P2["app"]                  = "30001"
        self.P2["code"]                 = result
        self.P2["keyCode"]              = "a9603ba96edd426eb47596f158eb579e"

    def get_result(self,ymdh,file_name):
        self.P2["type"]                 = "result"
        self.P2["from"]                 = ymdh
        self.P2["to"]                   = ymdh
        self.P2["tm"]                   = long(time.time()) * 1000
        s = self.P2.get("app") + self.P2.get("code") + str(self.P2.get("tm")) + \
            self.P2.get("from") + self.P2.get("to") + self.secretKey + self.P2.get("keyCode")
        
        self.P2['sign']         = hashlib.md5(s).hexdigest()
        url                     = self.log_url + "?" + urllib.urlencode(self.P2)
        result                  = urllib2.urlopen(url).read()
        R                       = json.loads(result)
        S                       = json.loads(urllib2.urlopen(R['check_link']).read())
        links_dict              = S['links']
        for link_dict in links_dict:
            link = link_dict['link']
            all_data = urllib2.urlopen(link).read()
            try:
                f = file(file_name,'a+')
                f.write(all_data)
                f.close()
            except:
                pass





if __name__ == "__main__":
    table_name  = "21623"
    file_path   = "data"
    file_name   = "user_action.%s.log"
    keep_day    = 6
    local       = True
    ymdh        = time.strftim("%Y%m%d%H",time.localtime())
    for day in [27,28,29]:
        for hour in range(24):
            ymdh = "201804%s%s" % (str(day).zfill(2), str(hour).zfill(2))
            file_name_final   = os.path.join(file_path, file_name%(ymdh))
            if os.path.exists(file_name_final):
                if check_file(file_name_final):
                    print file_name_final
                    continue
            init_filename(file_name_final)
            fail_file = clear_file(file_path,keep_day)
            if len(fail_file) > 0:
                print "Failed To Delete:",fail_file
            result,t,e = get_data(table_name, file_name_final, ymdh, local)
            if t:
                print "%s: Cost Time: %3.4fMin"%(ymdh,t/60)
            else:
                print "%s Get The Exception: %3"%(ymdh,e)




