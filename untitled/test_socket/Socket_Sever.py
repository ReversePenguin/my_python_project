#_*_ coding:utf-8 _*_

#服务器代码
import SocketServer

class MySever(SocketServer.BaseRequestHandler):
    #交互代码
    def handle(self):
        #客户端socket
        conn = self.request


        conn.close()




if __name__ == '__main__':
    sever = SocketServer.ThreadingTCPServer(('127.0.0.1',9999),MySever)
    sever.serve_forever()