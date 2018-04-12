#_*_ coding:utf-8 _*_

#服务器代码
import SocketServer
import os

class MySever(SocketServer.BaseRequestHandler):
    #交互代码
    def handle(self):
        base_path = r'D:\study\Python\PycharmProjects\untitled\test_socket\down_up_loads\temp'
        #客户端socket
        conn = self.request
        print 'connected...'
        while True:
            pre_data = conn.recv(1024)
            #获取请求方法、文件名、文件大小
            file_name,file_size = pre_data.split('|')
            #已经接收文件的大小
            recv_size = 0
            #上传文件路径拼接
            file_dir = os.path.join(base_path,file_name)
            print file_dir
            f = file(file_dir,'w')
            Flag = True
            while Flag:
                #未上传完毕
                if int(file_size) > recv_size:
                    #最多接收1024，可能接收的小于1024
                    data = conn.recv(1024)
                    recv_size += len(data)
                    f.write(data)
                #上传完毕，则退出循环
                else:
                    recv_size = 0
                    Flag = False
                #写入文件


            print 'upload successed.'
            f.close()

        #关闭
        conn.close()




if __name__ == '__main__':
    sever = SocketServer.ThreadingTCPServer(('127.0.0.1',9999),MySever)
    sever.serve_forever()