#!/usr/bin/env python
#_*_ coding:utf-8 _*_


import re

#查找ip地址
ip = 'sdhflah192.168.1.1uwehoehwf89.234.23.jdskf192.168.35.89vnai54.dfjo65.32.fjsdoj45'
print re.findall('(?:\d{1,3}\.){3}\d{1,3}',ip)  #?:表示取消分组编号

num1 = '1234567890'
num11 = '1123123123'
print re.findall('((?<=\d)\d{3})',num1)
#print re.findall('((?<=\d)\d{3})',num11)

num2 = ' 1 1 2 2 3 4 5 6'
print re.findall('(?<=\s)\d+(?=\s)',num2)

num3 = '1213456t789y'
print re.findall('\d{3}(?!\d)',num3)

str1 = 'I\'m singing while you\'re dancing.'
com = re.compile(r'\bsing\w*\b')
print re.findall(r'\b\w+(?=ing\b)',str1)
print com.findall(str1)

str2 = 'go st go'
print re.findall(r'\b(\w+)\b.*\1\b',str2)

str3 = '''
<li>
<a href="javascript:;" class="js-signup-noauth"><i class="zg-icon zg-icon-dd-home"></i>注册知乎</a>
</li>
<li>
<a href="javascript:;" class="js-signin-noauth">登录</a>
</li>
'''
str4 = r'<li>href="javascript:;" class="js-signin-noauth">登录</a></li>'
print (re.findall('(?<=<%s>\n).*(?=\n<\/%s>)' % ('li','li'),str3))[1]











