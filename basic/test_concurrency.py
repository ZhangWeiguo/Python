# -*- encoding:utf-8 -*-
import sys,urllib2,time
from threading_pool import ThreadingPool
from processing_pool import ProcessingPool
def fun(url):
    t1 = time.time()
    urllib2.urlopen(url).read()
    t2 = time.time()
    return t2 - t1

if __name__ == "__main__":
    data = sys.argv
    if len(data) == 4:
        url = data[1]
        threads = int(data[2])
        nums = int(data[3])
        print data
    else:
        print "Parameter Error"
        sys.exit(1)
    
    # print "================================================="
    # print "Under The Multi Threads:"
    # P = ThreadingPool(nums)
    # for i in range(nums):
    #     P.add_job(fun, url = url)
    # start_time = time.time()
    # P.start_job()
    # P.wait_complete()
    # end_time = time.time()
    # result = P.result_queue
    # T = []
    # while True:
    #     try:
    #         t = result.get(timeout=0.1)
    #         T.append(t)
    #     except:
    #         break
    # print "All %d Requests, %d Threads"%(nums,threads)
    # print "Main Avg Time Cost %2.5f"%((end_time-start_time)/len(T))
    # print "Request Max Time Cost %2.5f"%max(T)
    # print "Request Min Time Cost %2.5f"%min(T)
    # print "Request Avg Time Cost %2.5f"%(sum(T)/len(T))

    print "================================================="
    print "Under The Multi Process:"
    def callback(t):
        T.append(t)
    T = []
    P = ProcessingPool(nums)
    for i in range(nums):
        P.add_job(fun, callback=callback,url = url)

    start_time = time.time()
    P.start_job()
    P.wait_complete()
    end_time = time.time()
    print "All %d Requests, %d Process"%(nums,threads)
    print "Main Avg Time Cost %2.5f"%((end_time-start_time)/len(T))
    print "Request Max Time Cost %2.5f"%max(T)
    print "Request Min Time Cost %2.5f"%min(T)
    print "Request Avg Time Cost %2.5f"%(sum(T)/len(T))


    print "================================================="
    print "Under The One Threads:"
    start_time = time.time()
    T = []
    for i in range(nums):
        T.append(fun(url))
    end_time = time.time()
    print "Main Avg Time Cost %2.5f"%((end_time-start_time)/len(T))
    print "Request Max Time Cost %2.5f"%max(T)
    print "Request Min Time Cost %2.5f"%min(T)
    print "Request Avg Time Cost %2.5f"%(sum(T)/len(T))

    '''
    py -2 test_concurrency.py http://www.baidu.com 100 200
    多线程比单线程实际要慢，虽然支持了并发
    '''