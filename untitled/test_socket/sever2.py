#_*_ coding:utf-8 _*_

#可以同时处理多个客户端
import SocketServer

class MySever(SocketServer.BaseRequestHandler):
    def setup(self):
        pass

    def handle(self):
        #self.request
        #self.client_address
        #self.server
        conn = self.request
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

    def finish(self):
        pass


if __name__ == '__main__':
    sever = SocketServer.ThreadingTCPServer(('127.0.0.1',9999),MySever)
    sever.serve_forever()