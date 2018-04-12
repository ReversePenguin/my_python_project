#_*_ coding:utf-8 _*_
import redis

conn = redis.Redis(host= '127.0.0.1')
name = raw_input('enter your name:')
conn.set('name',str(name))
print conn.get('name')


