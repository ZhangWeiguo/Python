# -*- encoding:utf-8 -*-
from multiprocessing.pool import Pool

class ProcessingPool(Pool):
    def __init__(self,process_num):
        Pool.__init__(self,process_num)
        self.process_num = process_num
    def add_job(self,task,callback = None, **kwargs):
        self.apply_async(func = task,kwds=kwargs,callback=callback)
    def start_job(self):
        self.close()
    def wait_complete(self):
        self.join()
    

 
import os  
import random  
import time  
  
def worker(num):  
    for i in range(5):  
        print('===pid=%d==num=%d='%(os.getpid(),num))  
        time.sleep(1)
 
if __name__ == "__main__":
    pool=ProcessingPool(5)
    for i in range(10):  
        print('---%d---'%i)  
        pool.add_job(worker,num=i)  
    pool.start_job()
    pool.wait_complete()

