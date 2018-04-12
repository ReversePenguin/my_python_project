#_*_ coding:utf-8 _*_

from multiprocessing import Process,Queue
import Queue as Queue2

def f(q,n):
    q.put([n,'hello'])

if __name__ == '__main__':
    #共享队列，如果这么是import Queue，那么队列不共享，每个进程都会创建一个Queue
    print '-------multiprocessing封装的Queue-------'
    q = Queue()
    for i in range(5):
        p = Process(target=f,args=[q,i])
        p.start()
        p.join()
        print q.qsize()
    print 'out:',q.qsize()
    '''
    print q.qsize()
    while q.qsize():
        print q.get()

    '''
    print '-------multiprocessing封装的Queue-------'
    q = Queue2.Queue()
    for i in range(5):
        p = Process(target=f,args=[q,i])
        p.start()
        p.join()
        print q.get()
        print q.qsize()
    print 'out:',q.qsize()