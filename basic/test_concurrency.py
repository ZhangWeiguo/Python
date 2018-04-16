from multiprocessing import Pool,freeze_support
import os, time
import urllib2
import threading
import thread

Lock = threading.RLock()

def threads(task, thread_num = 10):
    t1 = time.time()
    for i in range(10):
        thread.start_new_thread(task,())
    t2 = time.time()
    all_cost_time = t2 - t1
    print "Avg Reauest Cost Time: %2.3f" % (all_cost_time / thread_num)


def threadings(task, thread_num = 10):
    t1 = time.time()
    p = []
    for i in range(thread_num):
        p.append(threading.Thread(target=task))
    for i in p:
        i.start()
    for i in p:
        i.join()
    t2 = time.time()
    all_cost_time = t2 - t1
    Lock.acquire()
    print "Avg Reauest Cost Time: %2.3f" % (all_cost_time / thread_num)
    Lock.release()



def process(task, process_num=10, all_num =100):
    t1 = time.time()
    p = Pool(process_num)
    T = []
    for i in range(all_num):
        T.append(p.apply_async(task))
    print 'Waiting for all subprocesses done...'
    p.close()
    p.join()
    print 'All subprocesses done.'
    t2 = time.time()
    all_cost_time = t2 - t1
    every_cost_time = [i.get() for i in T]
    print "One Reauest Cost Time: %2.3f" % (sum(every_cost_time)/all_num)
    print "Avg Reauest Cost Time: %2.3f" % (all_cost_time/all_num)


def fun1():
    t1 = time.time()
    a = urllib2.urlopen("http://www.baidu.com").read()
    time.sleep(3)
    t2 = time.time()
    print t2 - t1
    return t2 - t1

def fun2():
    t1 = time.time()
    f = file('test.txt', 'a+')
    f.writelines(["I am zhangweiguo\n"]*10)
    f.close()
    time.sleep(3)
    t2 = time.time()
    print t2 - t1
    return t2 - t1

if __name__ == "__main__":
    # process(fun1,10,20)
    # fun()
    threadings(fun2,10)
