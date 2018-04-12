#_*_ coding:utf-8 _*_

import socket

client = socket.socket()
ip_port = ('127.0.0.1',9999)
#连接端口
client.connect(ip_port)
#接收数据，最大为1024，返回的是字符串类型
data = client.recv(1024)
print data
while True:
    inf = raw_input('client:')
    #向服务端发送
    client.send(inf)
    print client.recv(1024)
    if inf == 'exit':
        break


