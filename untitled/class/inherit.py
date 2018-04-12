#_*_ coding:utf-8 _*_

class Father(object):
    
    def __init__(self):
        self.Fname = 'father'
        print 'father.__init__'
        
    def Func(self):
        print 'father.func'
        
    def Bad(self):
        print 'father.抽烟喝酒'
        

class Son(Father):
    
    def __init__(self):
        self.Sname = 'son'
        Father.__init__(self)
        #这种方法调用父类的构造函数需要父类继承object
        #super(Son,self).__init__() 
    
    def bar(self):
        print 'son.bar'
    
    #对父类的方法进行重写，调用时调用这个，如果不重写，则直接调用父类的
    def Bad(self):
        #执行父类的方法
        Father.Bad(self)
        #自己的方法
        print 'son.打架'
        
    
    

''''''
s1 = Son()


s1.bar()
s1.Func()
print s1.Sname
s1.Bad()





        
        
        
        
        
        
        
        
        
        
