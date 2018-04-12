#_*_ coding:utf-8 _*_

#class A(object):
class A:
    def __init__(self):
        print 'this is A'
        
    def Save(self):
        print 'A.save()'
        
class B(A):
    def __init__(self):
        print 'this is B'
    
        
class C(A):
    def __init__(self):
        print 'this is C'
        
    def Save(self):
        print 'C.save()'
        
class D(B,C):
    def __init__(self):
        print 'this is D'

d = D()
d.Save()
        

        
        
        
        
        
        
        
        
        
        