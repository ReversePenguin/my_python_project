#_*_ coding:utf-8 _*_

#生产者-消费者模型

from threading import Thread
from Queue import Queue
import time

class Producer(Thread):
    def __init__(self,name,queue):
        self.__name = name
        self.__queue = queue
        super(Producer, self).__init__()
        
    def run(self):
        #Thread.run(self)
        while True:
            if self.__queue.full():
                print '包子满了'
                time.sleep(10)
            else:
                print self.__name+'做了一个包子'
                self.__queue.put('包子')
                print '包子总数：' + str(self.__queue.qsize())
                time.sleep(1)




class Consumer(Thread):
    def __init__(self,name,queue):
        self.__name = name
        self.__queue = queue
        super(Consumer, self).__init__()

    def run(self):
        #Thread.run(self)
        while True:
            if self.__queue.empty():
                print '包子没有了'
                time.sleep(10)
            else:
                print self.__name+'吃了一个包子'
                self.__queue.get()
                time.sleep(1)

que = Queue(100)

p1 = Producer('X1',que)
p1.start()
p2 = Producer('X2',que)
p2.start()
p3 = Producer('X3',que)
p3.start()

for i in range(21):
    name = '顾客%d' % (i+1)
    c = Consumer(name,que)
    c.start()




'''
#创建队列
que = Queue(maxsize=100)
#返回队列中含有多少个数据
print que.qsize()
#往队列放数据
que.put('1')
que.put('2')
print que.qsize()
#取数据，一次一个，返回队列中的第一个（先进先出）
print 'get:',que.get()
print que.qsize()
print 'get:',que.get()
#返回是否为空
print 'empty',que.empty()

'''




