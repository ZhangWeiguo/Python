import time
from logger import LogClient,LogServer

def test1():
    import time
    logger = LogClient("Test","test", rotate = "Time", when = 'M', keepNum = 48)
    while True:
        logger.error("zhangweiuoerror")
        logger.info("zhangweiuoinfo")
        logger.debug("zhangweiuodebug")
        logger.warning("zhangweiuowarning")
        logger.fatal("zhangweiuofatal")
        time.sleep(10)

def test2():
    logger = LogServer(appName = 'test', keepNum = 24, bufferNum = 100)
    while True:
        logger.log(time.strftime("%Y%m%d %H:%M:%S") + "zhangweiuoinfo")
        time.sleep(0.1)

if __name__ == "__main__":
    test2()

