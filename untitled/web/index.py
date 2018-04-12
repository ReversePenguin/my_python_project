#_*_ coding:utf-8 _*_

import socket

def handle(client):
    data = client.recv(1024)
    # 下面两句是向浏览器说明你发的是html语言，不过一般浏览器不用写这个
    client.send("HTTP/1.1 200 OK\r\n")
    client.send("Content-Type:text/html\r\n\r\n")


    client.send("<a href = 'http://www.baidu.com'> 百度</a>")


def main():
    sock = socket.socket()#socket.AF_INET,socket.SOCK_STREAM)
    sock.bind(('localhost',8080))
    sock.listen(5)

    while True:
        conn,address = sock.accept()
        handle(conn)
        conn.close()

if __name__ == '__main__':
    main()


