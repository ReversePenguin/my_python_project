#_*_ coding:utf-8 _*_

#不能同时处理多个客户端
import socket

#建立socket对象
sk = socket.socket()
ip_port = ('127.0.0.1',9999)
#监听ip端口
sk.bind(ip_port)
#最大监听数，一般为5，大于5就堵塞
sk.listen(5)

#一直监听
while True:
    #获得访问的客户端的socket对象和ip端口，并阻塞（等待客户端操作）
    conn,address = sk.accept()
    #向客户端发送信息
    conn.send('sever: hello')
    flag = True
    while flag:
        #也有阻塞功能，等待客户端操作
        data = conn.recv(1024)
        print data
        if data == 'exit':
            flag = False
            conn.send('bye')
        conn.send('nobody')
    #关闭
    conn.close()


