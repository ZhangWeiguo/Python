import threading
import Queue

class ThreadingUnit(threading.Thread):
    def __init__(self, name, task, work_queue, result_queue = None,*args,**kwargs):
        threading.Thread.__init__(self, args=args,kwargs=kwargs)
        self.work_queue     = work_queue
        self.result_queue   = result_queue
        self.name           = name
        self.task           = task
        self.setDaemon(True)
        self.__notpause = threading.Event()
        self.__notstop = threading.Event()
        self.__notpause.set()
        self.__notstop.set()

    def run(self):
        while self.__notstop.isSet():
            self.__notpause.wait()
            try:
                result = self.task(self.work_queue)
                if self.result_queue:
                    self.result_queue.put(result)
            except Queue.Empty:
                break
            except:
                pass

    def pause(self):
        self.__notpause.clear()
    def goon(self):
        self.__notpause.set()
    def stop(self):
        self.__notpause.set()
        self.__notstop.clear()





class ThreadingPool:
    def __init__(self, task, num_threads = 10):
        self.num_threads = num_threads
        self.work_queue = Queue.Queue()
        self.result_queue = Queue.Queue()
        self.task = task
        self.threads = []
        for i in range(num_threads):
            t = ThreadingUnit("Threading %d"%i,task,self.work_queue, self.result_queue)
            self.threads.append(t)
    def add_job(self,**kwargs):
        self.work_queue.put((kwargs))

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
    def task(messages):
        lock.acquire()
        message = messages.get(timeout=0.2)
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
    P = ThreadingPool(task=task,num_threads=10)
    for i in range(100):
        s = random_string()
        P.add_job(message = s)
    P.start_job()
    # P.wait_complete()
    while True:
        t2 = time.time()
        if t2 - t1 > 10:
            import sys
            print t2 - t1
            print P.result_queue.qsize()
            sys.exit(1)

