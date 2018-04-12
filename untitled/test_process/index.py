#_*_ coding:utf-8 _*_

from multiprocessing import Process
from threading import Thread

def run(li,n):
    li.append(n)
    print li

if __name__ == '__main__':
    li = []
    print '------进程------'
    for i in range(10):
        p = Process(target=run,args=[li,i])
        p.start()
        p.join()
    print '------线程------'
    for i in range(10):
        p = Thread(target=run,args=[li,i])
        p.start()
        p.join()


