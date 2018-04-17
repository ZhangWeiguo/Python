import threading
import Queue

class ThreadingUnit(threading.Thread):
    def __init__(self, name, work_queue, result_queue, timeout = 30,**kwargs):
        threading.Thread.__init__(self, kwargs=kwargs)
        self.timeout        = timeout
        self.work_queue     = work_queue
        self.result_queue   = result_queue
        self.name           = name
        self.setDaemon(True)

    def run(self):
        while True:
            try:
                task,kwargs = self.work_queue.get(timeout = self.timeout)
                result = task(**kwargs)
                self.result_queue.put(result)
            except Queue.Empty:
                break
            except:
                pass




class ThreadingPool:
    def __init__(self, num_threads = 10):
        self.num_threads = num_threads
        self.work_queue = Queue.Queue()
        self.result_queue = Queue.Queue()
        self.threads = []
        for i in range(num_threads):
            t = ThreadingUnit("Threading %d"%i,self.work_queue, self.result_queue)
            self.threads.append(t)
    def add_job(self,task,**kwargs):
        self.work_queue.put((task,kwargs))

    def start_job(self):
        for i in self.threads:
            i.start()

    def wait_complete(self):
        while len(self.threads):
            thread = self.threads.pop()
            if thread.isAlive():
                thread.join()





if __name__ == "__main__":
    import random, time
    def task(message):
        lock.acquire()
        print time.strftime("%H:%M:%S", time.localtime()), message
        lock.release()
        time.sleep(1)

    def random_string():
        s = ""
        for i in range(10):
            s += random.choice("qwertyuioplkjhgfdsazcxvcbnm")
        return s
    t1 = time.time()
    lock = threading.RLock()
    P = ThreadingPool(10)
    for i in range(100):
        s = random_string()
        P.add_job(task,message = s)
    P.start_job()
    # P.wait_complete()
    while True:
        t2 = time.time()
        if t2 - t1 > 10:
            import sys
            print t2 - t1
            print P.result_queue.qsize()
            sys.exit(1)

