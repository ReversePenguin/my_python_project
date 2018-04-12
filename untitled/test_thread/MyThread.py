#_*_ coding:utf-8 _*_

from threading import Thread
import time

class MyTread(Thread):

    #重写了run方法，因此，原来的效果就会被覆盖
    def run(self):
        #调用父类的方法
        Thread.run(self)
        #自己添加的程序
        print '我的线程'



def Foo(arg1,arg2):
    print 'Foo()',arg1,arg2

t1 = MyTread(target=Foo,args=(1,2,))
t1.start()




