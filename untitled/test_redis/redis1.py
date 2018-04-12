#_*_ coding:utf-8 _*_

import redis

class RedisHelper:
#redis的发布订阅功能
    def __init__(self):
        #连接服务器
        self.__conn = redis.Redis(host='127.0.0.1')
        #设置收发的频道
        self.chan_sub = 'fm104.5'
        self.chan_pub = 'fm104.5'

    def get(self,key):
        #返回key的值
        return self.__conn.get(key)

    def set(self,key,value):
        #设置key的值
        self.__conn.set(key,value)

    def publish(self,msg):
        #向频道发送消息
        self.__conn.publish(self.chan_pub,msg)
        return True

    def subscribe(self):
        #连接频道查看状态
        pub = self.__conn.pubsub()
        #订阅
        pub.subscribe(self.chan_sub)
        #等待接受消息
        pub.parse_response()
        return pub

if __name__ == '__main__':
    t = RedisHelper()
    t.publish('i am coming')







