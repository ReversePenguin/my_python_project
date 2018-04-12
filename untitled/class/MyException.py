#_*_ coding:utf-8 _*_

class MyException(Exception):
    
    def __init__(self,mgs):
        self.error = mgs
    
    #可以直接print对象名返回这里的return    
    def __str__(self, *args, **kwargs):
        return self.error
    
a = MyException('自定义错误信息')
print a
#主动触发异常
#raise MyException('主动触发的异常')
        