# -*- encoding:utf-8 -*-
import logging,time,sys,os,platform
from logging.handlers import TimedRotatingFileHandler,RotatingFileHandler

'''
logger = logClient("Test","test", rotate = "Time", when = 'H', keepNum = 48)
logger = logClient("Test","test", rotate = "Size", maxBytes = 1028, keepNum = 48)
logger = logClient("Test","test", rotate = "None")
'''




class logClient:
    def __init__(self, 
            appName, 
            fileName, 
            rotate      =   "None", 
            when        =   'H', 
            keepNum     =   24, 
            maxBytes    =   1024*1024*10,
            maxBuffer   =   100 ):
        '''
        rotate : None,Time,Size
        '''
        self.logger = logging.getLogger(appName)
        self.fileName = fileName
        self.appName = appName
        formater = logging.Formatter(
            fmt         = "%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)-8s %(message)s",
            datefmt     = "%Y-%m-%d %H:%M:%S")
        
        if rotate == 'Time':
            fileHandler = TimedRotatingFileHandler(fileName, 
                                                    when        =   when, 
                                                    interval    =   1, 
                                                    backupCount =   keepNum)
            fileHandler.suffix = "%Y%m%d%H%M.log"
        elif rotate == 'Size':
            fileHandler = RotatingFileHandler(filename = fileName, 
                                            maxBytes = maxBytes, 
                                            backupCount = keepNum)
        else:
            fileHandler = logging.FileHandler(filename = fileName)

        fileHandler.formatter = formater
        self.logger.addHandler(fileHandler)
        self.logger.setLevel(logging.DEBUG)
        self.logBuffer = []
        self.errorBuffer = []

        

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


class LogServer:
    def __init__(self, appName, keepNum = 24, bufferNum = 100):
        self.bufferNum = bufferNum
        self.buffer = []
        self.appName = appName
        self.fileName = "%s.%s.log"
        if 'Windows' in platform.system():
            isUnix = False
        else:
            import fcntl
    
    def log(self,data):
        num = len(self.buffer)
        if num <= self.bufferNum:
            if data.strip() != "":
                name = sys._getframe().f_back.f_code.co_filename
                line = str(sys._getframe().f_back.f_lineno)
                dt = time.strftime("%Y-%m-%d %H:%M:%S")
                s = "%15s %20s %5s  :  %s\n"%(dt, name, line, data)
                self.buffer.append(s)
        else:
            self.flush()
    
    def flush(self):
        ymdh = time.strftime("%Y%m%d%H")
        fileName = self.fileName%(self.appName, ymdh)
        f = file(fileName, 'a+')
        if isUnix:
            fcntl.flock(f, fcntl.LOCK_EX)
            f.writelines(self.buffer)
            fcntl.flock(f,fcntl.LOCK_UN)
        else:
            # windows 下未找到文件锁方式
            f.writelines(self.buffer)
        f.close()    
        self.buffer = []

            
        
