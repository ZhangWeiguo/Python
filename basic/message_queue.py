import Queue,threading,time,random
from itertools import chain
from threading_pool import ThreadingUnit

class MessageQueue:
    def __init__(self,
                 consumer,
                 producer,
                 num_consumer = 2,
                 num_producer = 2,
                 daemon = True,
                 timeout = 0.1):
        self.work_queue = Queue.Queue()
        self.result_queue = Queue.Queue()
        self.consumer = consumer
        self.producer = producer
        self.timeout = timeout
        self.consumer_threads = []
        self.producer_threads = []
        for i in range(num_consumer):
            self.consumer_threads.append(
                ThreadingUnit(name = "comsumer_%d"%i,
                              task = self.consumer,
                              work_queue = self.work_queue,
                              result_queue = self.result_queue,
                              timeout = self.timeout))
        for i in range(num_producer):
            self.producer_threads.append(
                ThreadingUnit(name = "producer_%d"%i,
                              task = self.producer,
                              work_queue = self.work_queue,
                              result_queue = self.result_queue,
                              timeout = self.timeout))
        if daemon:
            for thread in chain(self.consumer_threads,self.producer_threads):
                thread.setDaemon(True)
        else:
            for thread in chain(self.consumer_threads,self.producer_threads):
                thread.setDaemon(False)

    def start(self):
        for i in chain(self.consumer_threads,self.producer_threads):
            i.start()

    def pause(self):
        for i in chain(self.consumer_threads,self.producer_threads):
            i.pause()
    def goon(self):
        for i in chain(self.consumer_threads,self.producer_threads):
            i.goon()
    def stop(self):
        for i in chain(self.consumer_threads,self.producer_threads):
            i.stop()



def random_string():
    s = ""
    for i in range(10):
        s += random.choice("qwertyuioplkjhgfdsazcxvcbnm")
    return s
def get_time():
    return time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
def produce(q):
    s = random_string()
    q.put(s)
    lock.acquire()
    print "%s:%7s:%s"%(get_time(),"produce",s)
    lock.release()
    time.sleep(1)

def consume(q):
    s = q.get(timeout=10)
    lock.acquire()
    print "%s:%7s:%s"%(get_time(),"consume",s)
    lock.release()

def test():
    q = Queue.Queue()
    producer = threading.Thread(name = "producer", target = produce, args=(q,))
    consumer = threading.Thread(name = "consumer", target = consume, args=(q,))
    producer.setDaemon(True)
    consumer.setDaemon(True)
    producer.start()
    consumer.start()
    # producer.join()
    # consumer.join()
    time.sleep(10)

lock = threading.RLock()
mq = MessageQueue(consumer=consume, producer=produce)
mq.start()
t1 = time.time()
while True:
    if time.time() - t1 < 5:
        pass
    elif time.time() -t1 >= 5 and time.time() - t1 <= 10:
        print "Begin to Pause"
        mq.pause()
        time.sleep(6)
    else:
        print "Begin to Goon"
        mq.goon()
        time.sleep(5)
    if time.time() - t1 >= 15:
        break

