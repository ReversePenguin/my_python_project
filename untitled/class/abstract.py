#_*_ coding:utf-8 _*_

from abc import ABCMeta,abstractmethod

class A :
    #抽象类
    __metaclass__ = ABCMeta
    
    #抽象方法，继承该抽象类的类必须重写这个方法。
    @abstractmethod
    def Send(self):pass
    
#抽象类+抽象方法 = 接口（第二种借口，即规范）


class B(A):
    def __init__(self):
        print 'this is B'
        
    def Send(self):
        print 'send.way'
        
        
b1 = B()
b1.Send()


