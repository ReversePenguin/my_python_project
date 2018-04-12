#_*_ coding:utf-8 _*_

import os,time
from multiprocessing import Process

def info(title):
    print title
    print 'module name:',__name__
    if hasattr(os,'getppid'):
        print 'parent process:',os.getppid()
    time.sleep(5)
    print 'process id:',os.getpid()

def f(name):
    info('function f')
    print 'hello',name

if __name__ == '__main__':
    info('main line')
    print '------------------------'
    p = Process(target=f,args=('john',))
    p.start()
    p.join()




