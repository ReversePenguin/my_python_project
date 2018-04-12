#_*_ coding:utf-8 _*_

from threading import Thread
import time

def Foo(arg):
    for i in range(100):
        print i
        time.sleep(1)

print 'before'
#创建一个线程并给线程传递要干的事加一个逗号就只是说明这是一个序列
#此为子线程，主线程为执行整个程序时创建
t1 = Thread(target=Foo,args=(1,))  #调用Thread类的run（）方法
#线程开始执行
t1.isDaemon()  #查看是否守护线程。0或者False表示被主线程保护线程中，即主程序的代码运行完成后，子程序继续运行，直到运行完成，主线程才停止
#t1.setDaemon(True)  #关闭线程保护，主程序运行完成后不管子线程运行完毕即刻关闭，
t1.start()
#t1.join()   #运行到这里执行子线程，直到完毕后，继续执行下面的程序
#t1.join(5)   #设置超时5s，5秒后就不管子线程运行完毕都暂停，执行之后的代码


print 'after'
print 'after'
print 'after'
print 'after end'
time.sleep(10)   #加入这个可以观察出，子线程在关闭前也是在运行的







