import logging
from logging.handlers import TimedRotatingFileHandler,RotatingFileHandler

class logClient:
    def __init__(self, appName, fileName, roate = "None", when ='H', keepNum = 24, maxBytes = 1024*1024*10 ):
        '''
        rotate : None,Time,Size
        '''
        self.logger = logging.getLogger(appName)
        self.fileName = fileName
        self.appName = appName
        formater = logging.Formatter(
            fmt         = "%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)-8s %(message)s",
            datefmt     = "%Y-%m-%d %H:%M:%S")
        
        if roate == 'Time':
            fileHandler = TimedRotatingFileHandler(fileName, 
                                                    when        =   when, 
                                                    interval    =   1, 
                                                    backupCount =   keepNum)
            fileHandler.suffix = "%Y%m%d%H%M.log"
        elif roate == 'Size':
            fileHandler = RotatingFileHandler(filename = fileName, 
                                            maxBytes = maxBytes, 
                                            backupCount = keepNum)
        else:
            fileHandler = logging.FileHandler(filename = fileName)

        fileHandler.formatter = formater
        self.logger.addHandler(fileHandler)
        self.logger.setLevel(logging.DEBUG)
        

    def info(self, message):
        self.logger.info(message)
    def error(self, message):
        self.logger.error(message)
    def debug(self, message):
        self.logger.debug(message)
    def warning(self, message):
        self.logger.warning(message)       
    def fatal(self, message):
        self.logger.fatal(message)
    def critical(self, message):
        self.logger.critical(message)    

if __name__ == "__main__":
    import time
    logger = logClient("No1","test", roate="Size", maxBytes=20)
    while True:
        logger.error("error")
        logger.info("info")
        logger.debug("debug")
        logger.warning("warning")
        logger.fatal("fatal")
        time.sleep(60)
