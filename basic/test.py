import multiprocessing,time,os
from logger import Logger

def test(process_name):
    logger = Logger("Test","test", rotate = "Time", when = 'M', keep_num = 5)
    k = 0
    pid = os.getpid()
    while True:
        k += 1
        message = "%3d %6d %s"%(k, pid, process_name)
        logger.info(message)
        time.sleep(1)
if __name__ == "__main__":
    q1 = multiprocessing.Process(target=test, kwargs={"process_name":"process one"})
    q1.start()


